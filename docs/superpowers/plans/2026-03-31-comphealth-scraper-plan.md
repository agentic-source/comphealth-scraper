# CompHealth Daily Job Scraper Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a daily automated system that scrapes new CompHealth job postings, identifies the likely facility via Claude API, and emails a formatted report each weekday morning to tyler@connecthealthstaff.com.

**Architecture:** Three Python scripts (`scraper.py`, `identifier.py`, `emailer.py`) communicate via temp JSON files. A shared `state.py` module manages deduplication state. A GitHub Actions workflow orchestrates the daily run and commits updated state back to the repo.

**Tech Stack:** Python 3.11+, Playwright (headless Chromium), Anthropic Python SDK (`claude-haiku-4-5-20251001`), smtplib / SendGrid, pytest

**Spec:** `docs/superpowers/specs/2026-03-31-comphealth-scraper-design.md`

---

## File Map

| File | Responsibility |
|---|---|
| `comphealth-scraper/scraper.py` | Playwright scraper → writes `jobs_new.json`, updates `state.json` |
| `comphealth-scraper/identifier.py` | Claude API → reads `jobs_new.json`, writes `jobs_enriched.json` |
| `comphealth-scraper/emailer.py` | Email → reads `jobs_enriched.json`, sends HTML table; also handles `--failure` mode |
| `comphealth-scraper/state.py` | Load/save/prune/deduplicate `state.json` |
| `comphealth-scraper/state.json` | Initial empty state: `[]` |
| `comphealth-scraper/requirements.txt` | Python dependencies |
| `comphealth-scraper/.gitignore` | Ignores `jobs_new.json`, `jobs_enriched.json` |
| `comphealth-scraper/tests/test_state.py` | Unit tests for state.py |
| `comphealth-scraper/tests/test_identifier.py` | Unit tests for identifier.py |
| `comphealth-scraper/tests/test_emailer.py` | Unit tests for emailer.py |
| `.github/workflows/daily-scrape.yml` | Cron schedule, runs scripts, commits state |

**Inter-process data format:**

`jobs_new.json` and `jobs_enriched.json` are written to the `comphealth-scraper/` directory and gitignored. Each is a JSON array:

```json
// jobs_new.json — written by scraper.py, read by identifier.py
[
  {
    "id": "job-12345",
    "title": "Cardiologist Needed in Texas",
    "city": "Austin",
    "state": "TX",
    "specialty": "Cardiology",
    "job_type": "Locum Tenens",
    "compensation": "$200-250/hr",
    "description_bullets": ["12-week assignment", "50 patients/day"],
    "url": "https://www.comphealth.com/jobs/job-12345"
  }
]

// jobs_enriched.json — written by identifier.py, read by emailer.py
// Same as above but each job has an "identification" key added:
{
  "identification": {
    "facility_name": "St. David's Medical Center",
    "facility_type": "Community Hospital",
    "confidence": "high",
    "reasoning": "Only major cardiac center in Austin at this rate",
    "alternative_facility": "Ascension Seton Medical Center Austin"
  }
}
```

---

## Task 1: Project Scaffold

**Files:**
- Create: `comphealth-scraper/requirements.txt`
- Create: `comphealth-scraper/state.json`
- Create: `comphealth-scraper/.gitignore`
- Create: `comphealth-scraper/tests/__init__.py`

- [ ] **Step 1: Create the directory structure**

```bash
mkdir -p comphealth-scraper/tests
touch comphealth-scraper/tests/__init__.py
```

- [ ] **Step 2: Create `comphealth-scraper/requirements.txt`**

```
anthropic>=0.40.0
playwright>=1.44.0
sendgrid>=6.11.0
pytest>=8.0.0
pytest-mock>=3.14.0
```

- [ ] **Step 3: Create `comphealth-scraper/state.json`**

```json
[]
```

- [ ] **Step 4: Create `comphealth-scraper/.gitignore`**

```
jobs_new.json
jobs_enriched.json
__pycache__/
*.pyc
.pytest_cache/
```

- [ ] **Step 5: Install dependencies**

```bash
cd comphealth-scraper
pip install -r requirements.txt
playwright install chromium
```

Expected: all packages install without error, Chromium downloads successfully.

- [ ] **Step 6: Commit**

```bash
git add comphealth-scraper/
git commit -m "feat: scaffold comphealth-scraper project"
```

---

## Task 2: State Management (`state.py`)

**Files:**
- Create: `comphealth-scraper/state.py`
- Create: `comphealth-scraper/tests/test_state.py`

- [ ] **Step 1: Write the failing tests**

Create `comphealth-scraper/tests/test_state.py`:

```python
import json
import pytest
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import patch


def make_entry(job_id: str, days_ago: int = 0) -> dict:
    d = (datetime.today() - timedelta(days=days_ago)).strftime("%Y-%m-%d")
    return {"id": job_id, "seen_date": d}


class TestLoadState:
    def test_returns_empty_list_when_file_missing(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        import state
        with patch.object(state, "STATE_FILE", tmp_path / "state.json"):
            assert state.load_state() == []

    def test_returns_entries_from_existing_file(self, tmp_path):
        import state
        entries = [make_entry("job-1"), make_entry("job-2")]
        state_file = tmp_path / "state.json"
        state_file.write_text(json.dumps(entries))
        with patch.object(state, "STATE_FILE", state_file):
            assert state.load_state() == entries


class TestSaveState:
    def test_prunes_entries_older_than_60_days(self, tmp_path):
        import state
        state_file = tmp_path / "state.json"
        entries = [
            make_entry("job-old", days_ago=61),
            make_entry("job-new", days_ago=1),
        ]
        with patch.object(state, "STATE_FILE", state_file):
            state.save_state(entries)
            result = json.loads(state_file.read_text())
        assert len(result) == 1
        assert result[0]["id"] == "job-new"

    def test_deduplicates_by_id(self, tmp_path):
        import state
        state_file = tmp_path / "state.json"
        entries = [make_entry("job-1"), make_entry("job-1")]
        with patch.object(state, "STATE_FILE", state_file):
            state.save_state(entries)
            result = json.loads(state_file.read_text())
        assert len(result) == 1

    def test_keeps_entries_within_60_days(self, tmp_path):
        import state
        state_file = tmp_path / "state.json"
        entries = [make_entry("job-1", days_ago=59), make_entry("job-2", days_ago=60)]
        with patch.object(state, "STATE_FILE", state_file):
            state.save_state(entries)
            result = json.loads(state_file.read_text())
        assert {e["id"] for e in result} == {"job-1", "job-2"}


class TestGetSeenIds:
    def test_returns_set_of_ids(self, tmp_path):
        import state
        state_file = tmp_path / "state.json"
        entries = [make_entry("job-1"), make_entry("job-2")]
        state_file.write_text(json.dumps(entries))
        with patch.object(state, "STATE_FILE", state_file):
            assert state.get_seen_ids() == {"job-1", "job-2"}

    def test_returns_empty_set_when_no_state(self, tmp_path):
        import state
        with patch.object(state, "STATE_FILE", tmp_path / "state.json"):
            assert state.get_seen_ids() == set()


class TestAddJobs:
    def test_appends_new_job_ids_to_state(self, tmp_path):
        import state
        state_file = tmp_path / "state.json"
        state_file.write_text(json.dumps([make_entry("job-existing")]))
        jobs = [{"id": "job-new"}]
        with patch.object(state, "STATE_FILE", state_file):
            state.add_jobs(jobs)
            result = json.loads(state_file.read_text())
        ids = {e["id"] for e in result}
        assert ids == {"job-existing", "job-new"}
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
cd comphealth-scraper
python -m pytest tests/test_state.py -v
```

Expected: `ModuleNotFoundError: No module named 'state'`

- [ ] **Step 3: Create `comphealth-scraper/state.py`**

```python
import json
from datetime import datetime, timedelta
from pathlib import Path

STATE_FILE = Path(__file__).parent / "state.json"


def load_state() -> list[dict]:
    if not STATE_FILE.exists():
        return []
    with open(STATE_FILE) as f:
        return json.load(f)


def save_state(entries: list[dict]) -> None:
    cutoff = (datetime.today() - timedelta(days=60)).strftime("%Y-%m-%d")
    pruned = [e for e in entries if e["seen_date"] >= cutoff]
    deduped = list({e["id"]: e for e in pruned}.values())
    with open(STATE_FILE, "w") as f:
        json.dump(deduped, f, indent=2)


def get_seen_ids() -> set[str]:
    return {e["id"] for e in load_state()}


def add_jobs(jobs: list[dict]) -> None:
    today = datetime.today().strftime("%Y-%m-%d")
    existing = load_state()
    new_entries = [{"id": job["id"], "seen_date": today} for job in jobs]
    save_state(existing + new_entries)
```

- [ ] **Step 4: Run tests and verify they pass**

```bash
cd comphealth-scraper
python -m pytest tests/test_state.py -v
```

Expected: all 8 tests pass.

- [ ] **Step 5: Commit**

```bash
git add comphealth-scraper/state.py comphealth-scraper/tests/test_state.py
git commit -m "feat: add state management module with tests"
```

---

## Task 3: Scraper (`scraper.py`)

**Files:**
- Create: `comphealth-scraper/scraper.py`

Note: Playwright is difficult to unit test with mocks. The scraper is tested manually (Step 4). CSS selectors are discovered in Step 1 using the browser tool.

- [ ] **Step 1: Discover CSS selectors by inspecting comphealth.com**

Run this exploration script to find the right selectors before writing scraper.py:

```python
# explore_selectors.py (delete after use)
import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # visible for inspection
        page = await browser.new_page(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        )
        await page.goto("https://www.comphealth.com/jobs", wait_until="networkidle")

        # Print page title and first 5000 chars of HTML to identify job card structure
        print("Title:", await page.title())
        content = await page.content()
        print(content[:5000])

        input("Inspect the browser, then press Enter to continue...")
        await browser.close()

asyncio.run(main())
```

Run: `cd comphealth-scraper && python explore_selectors.py`

Record the CSS selectors for:
- Job card container
- Job title
- Location
- Specialty
- Job type
- Compensation
- Description bullets
- Job URL / ID
- Pagination next button
- Total job count display

Update the selectors in `scraper.py` (Step 2) based on findings.

- [ ] **Step 2: Create `comphealth-scraper/scraper.py`**

Replace `SELECTOR_*` constants with the actual selectors discovered in Step 1.

```python
import asyncio
import json
import random
import sys
from pathlib import Path
from playwright.async_api import async_playwright, Page

# Update these after running explore_selectors.py
SELECTOR_JOB_CARD = "article.job-card, [data-testid='job-card'], .job-listing-card"
SELECTOR_TITLE = "h2, h3, .job-title, [data-testid='job-title']"
SELECTOR_LOCATION = ".job-location, [data-testid='location'], .location"
SELECTOR_SPECIALTY = ".specialty, [data-testid='specialty']"
SELECTOR_JOB_TYPE = ".job-type, [data-testid='job-type'], .employment-type"
SELECTOR_COMPENSATION = ".compensation, [data-testid='compensation'], .salary"
SELECTOR_DESCRIPTION = "ul li, .job-details li, [data-testid='description'] li"
SELECTOR_JOB_LINK = "a[href*='/jobs/']"
SELECTOR_NEXT_PAGE = "button[aria-label='Next page'], a[aria-label='Next'], .pagination-next"
SELECTOR_TOTAL_COUNT = ".job-count, [data-testid='total-jobs'], h1"

JOBS_NEW_FILE = Path(__file__).parent / "jobs_new.json"
MIN_TOTAL_JOBS = 100


async def get_total_job_count(page: Page) -> int:
    """Return total jobs visible on the page. Returns 0 if not found."""
    try:
        el = page.locator(SELECTOR_TOTAL_COUNT).first
        text = await el.text_content(timeout=5000)
        # Extract first number found, e.g. "10,623 CompHealth jobs" → 10623
        import re
        match = re.search(r"[\d,]+", text or "")
        if match:
            return int(match.group().replace(",", ""))
    except Exception:
        pass
    return 0


async def extract_job_from_card(card) -> dict | None:
    """Extract job fields from a single job card element."""
    try:
        link_el = card.locator(SELECTOR_JOB_LINK).first
        href = await link_el.get_attribute("href") or ""
        job_id = href.rstrip("/").split("/")[-1]
        if not job_id:
            return None

        title = await _get_text(card, SELECTOR_TITLE)
        location_raw = await _get_text(card, SELECTOR_LOCATION)
        specialty = await _get_text(card, SELECTOR_SPECIALTY)
        job_type = await _get_text(card, SELECTOR_JOB_TYPE)
        compensation = await _get_text(card, SELECTOR_COMPENSATION)

        # Parse "City, ST" from location string
        city, state = "", ""
        if "," in location_raw:
            parts = location_raw.split(",", 1)
            city = parts[0].strip()
            state = parts[1].strip()[:2]

        # Description bullets
        bullets = []
        bullet_els = card.locator(SELECTOR_DESCRIPTION)
        count = await bullet_els.count()
        for i in range(min(count, 8)):
            text = await _get_text(bullet_els.nth(i), "")
            if text:
                bullets.append(text)

        base_url = "https://www.comphealth.com"
        full_url = href if href.startswith("http") else base_url + href

        return {
            "id": job_id,
            "title": title,
            "city": city,
            "state": state,
            "location": location_raw,
            "specialty": specialty,
            "job_type": job_type,
            "compensation": compensation,
            "description_bullets": bullets,
            "url": full_url,
        }
    except Exception as e:
        print(f"Warning: failed to extract job card: {e}", file=sys.stderr)
        return None


async def _get_text(element, selector: str) -> str:
    """Helper: get text from a locator, return empty string on failure."""
    try:
        if selector:
            el = element.locator(selector).first
        else:
            el = element
        text = await el.text_content(timeout=3000)
        return (text or "").strip()
    except Exception:
        return ""


async def scrape_all_jobs() -> tuple[list[dict], bool]:
    """
    Scrape all jobs posted today from comphealth.com.
    Returns (jobs, is_complete) where is_complete=False means pagination failed mid-way.
    """
    jobs = []
    is_complete = True

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
        )

        try:
            url = "https://www.comphealth.com/jobs?datePosted=today&sort=newest"
            await page.goto(url, wait_until="networkidle", timeout=30000)

            # Sanity check
            total = await get_total_job_count(page)
            if total < MIN_TOTAL_JOBS:
                raise RuntimeError(
                    f"Sanity check failed: only {total} total jobs visible "
                    f"(expected at least {MIN_TOTAL_JOBS}). Site may be blocked or changed."
                )

            # Paginate through all results
            page_num = 1
            while True:
                print(f"Scraping page {page_num}...", file=sys.stderr)
                cards = page.locator(SELECTOR_JOB_CARD)
                card_count = await cards.count()

                for i in range(card_count):
                    job = await extract_job_from_card(cards.nth(i))
                    if job:
                        jobs.append(job)

                # Check for next page
                next_btn = page.locator(SELECTOR_NEXT_PAGE).first
                if await next_btn.count() == 0 or not await next_btn.is_enabled():
                    break

                try:
                    await next_btn.click()
                    await page.wait_for_load_state("networkidle", timeout=15000)
                    await asyncio.sleep(random.uniform(1.0, 3.0))
                    page_num += 1
                except Exception as e:
                    print(f"Pagination failed on page {page_num}: {e}", file=sys.stderr)
                    is_complete = False
                    break

        finally:
            await browser.close()

    return jobs, is_complete


def main() -> None:
    import state as state_module

    seen_ids = state_module.get_seen_ids()

    try:
        all_jobs, is_complete = asyncio.run(scrape_all_jobs())
    except RuntimeError as e:
        # Sanity check failure or site unreachable
        print(f"SCRAPER_FATAL: {e}", file=sys.stderr)
        sys.exit(1)

    # Deduplicate against state
    new_jobs = [j for j in all_jobs if j["id"] not in seen_ids]

    # Write new jobs to temp file
    with open(JOBS_NEW_FILE, "w") as f:
        json.dump(new_jobs, f, indent=2)

    # Update state with all new IDs seen this run
    state_module.add_jobs(new_jobs)

    if not is_complete:
        print("SCRAPER_PARTIAL: pagination failed mid-way, results may be incomplete", file=sys.stderr)

    print(f"Found {len(new_jobs)} new jobs out of {len(all_jobs)} scraped total")


if __name__ == "__main__":
    main()
```

- [ ] **Step 3: Run a manual test scrape**

```bash
cd comphealth-scraper
python scraper.py
```

Expected output:
```
Scraping page 1...
Scraping page 2...
...
Found N new jobs out of M scraped total
```

Inspect `jobs_new.json` to verify job fields are populated correctly:
```bash
python -c "import json; jobs=json.load(open('jobs_new.json')); print(json.dumps(jobs[:2], indent=2))"
```

If the output shows empty fields (e.g., empty title, location), go back to Step 1 and update selectors.

- [ ] **Step 4: Reset state after testing**

```bash
echo '[]' > state.json
rm -f jobs_new.json
```

- [ ] **Step 5: Commit**

```bash
git add comphealth-scraper/scraper.py
git commit -m "feat: add Playwright scraper for comphealth.com"
```

---

## Task 4: Facility Identifier (`identifier.py`)

**Files:**
- Create: `comphealth-scraper/identifier.py`
- Create: `comphealth-scraper/tests/test_identifier.py`

- [ ] **Step 1: Write the failing tests**

Create `comphealth-scraper/tests/test_identifier.py`:

```python
import json
import pytest
from unittest.mock import MagicMock, patch


def make_job(**kwargs) -> dict:
    defaults = {
        "id": "job-1",
        "title": "Cardiologist Needed in Texas",
        "city": "Austin",
        "state": "TX",
        "specialty": "Cardiology",
        "job_type": "Locum Tenens",
        "compensation": "$200-250/hr",
        "description_bullets": ["12-week assignment", "50 patients/day"],
        "url": "https://www.comphealth.com/jobs/job-1",
    }
    return {**defaults, **kwargs}


def make_claude_response(data: dict) -> MagicMock:
    response = MagicMock()
    response.content = [MagicMock()]
    response.content[0].text = json.dumps(data)
    return response


class TestIdentifyFacility:
    def test_returns_structured_result_on_success(self):
        import identifier
        mock_client = MagicMock()
        mock_client.messages.create.return_value = make_claude_response({
            "facility_name": "St. David's Medical Center",
            "facility_type": "Community Hospital",
            "confidence": "high",
            "reasoning": "Only major cardiac center in Austin",
            "alternative_facility": "Ascension Seton",
        })
        result = identifier.identify_facility(mock_client, make_job())
        assert result["facility_name"] == "St. David's Medical Center"
        assert result["confidence"] == "high"
        assert "reasoning" in result

    def test_retries_once_on_invalid_json(self):
        import identifier
        mock_client = MagicMock()
        valid_response = make_claude_response({
            "facility_name": "Regional Hospital",
            "facility_type": "Hospital",
            "confidence": "medium",
            "reasoning": "Best match",
            "alternative_facility": None,
        })
        # First call returns invalid JSON, second returns valid
        mock_client.messages.create.side_effect = [
            MagicMock(content=[MagicMock(text="not valid json")]),
            valid_response,
        ]
        result = identifier.identify_facility(mock_client, make_job())
        assert result["facility_name"] == "Regional Hospital"
        assert mock_client.messages.create.call_count == 2

    def test_returns_unable_to_identify_after_two_failures(self):
        import identifier
        mock_client = MagicMock()
        mock_client.messages.create.return_value = MagicMock(
            content=[MagicMock(text="not json")]
        )
        result = identifier.identify_facility(mock_client, make_job())
        assert result["facility_name"] == "Unable to identify"
        assert result["confidence"] == "none"

    def test_returns_unable_to_identify_on_missing_required_keys(self):
        import identifier
        mock_client = MagicMock()
        # Response missing 'reasoning' key
        mock_client.messages.create.return_value = make_claude_response({
            "facility_name": "Some Hospital",
            "confidence": "high",
        })
        result = identifier.identify_facility(mock_client, make_job())
        assert result["facility_name"] == "Unable to identify"

    def test_alternative_facility_is_none_when_absent(self):
        import identifier
        mock_client = MagicMock()
        mock_client.messages.create.return_value = make_claude_response({
            "facility_name": "City Hospital",
            "facility_type": "Hospital",
            "confidence": "low",
            "reasoning": "Only hospital in area",
        })
        result = identifier.identify_facility(mock_client, make_job())
        assert result.get("alternative_facility") is None
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
cd comphealth-scraper
python -m pytest tests/test_identifier.py -v
```

Expected: `ModuleNotFoundError: No module named 'identifier'`

- [ ] **Step 3: Create `comphealth-scraper/identifier.py`**

```python
import json
import sys
import time
from pathlib import Path
import anthropic

JOBS_NEW_FILE = Path(__file__).parent / "jobs_new.json"
JOBS_ENRICHED_FILE = Path(__file__).parent / "jobs_enriched.json"

MODEL = "claude-haiku-4-5-20251001"

USER_PROMPT_TEMPLATE = """Identify the most likely US healthcare facility for this CompHealth job posting.
CompHealth anonymizes facility names, but you can infer the facility from location, specialty, compensation, and description details.

Job details:
Title: {title}
Location: {city}, {state}
Specialty: {specialty}
Job Type: {job_type}
Compensation: {compensation}
Details:
{description}

Respond with JSON only, no other text:
{{
  "facility_name": "Name of the most likely facility",
  "facility_type": "e.g. Community Hospital, Academic Medical Center, Critical Access Hospital",
  "confidence": "high or medium or low",
  "reasoning": "Brief explanation of why this facility matches the posting details",
  "alternative_facility": "Second most likely facility name, or null if none"
}}"""

REQUIRED_KEYS = {"facility_name", "confidence", "reasoning"}
FALLBACK = {
    "facility_name": "Unable to identify",
    "facility_type": "",
    "confidence": "none",
    "reasoning": "",
    "alternative_facility": None,
}


def identify_facility(client: anthropic.Anthropic, job: dict) -> dict:
    """Call Claude to identify the most likely facility for a job posting.
    Retries once on parse failure. Returns FALLBACK on second failure."""
    prompt = USER_PROMPT_TEMPLATE.format(
        title=job.get("title", ""),
        city=job.get("city", ""),
        state=job.get("state", ""),
        specialty=job.get("specialty", ""),
        job_type=job.get("job_type", ""),
        compensation=job.get("compensation", ""),
        description="\n".join(f"- {b}" for b in job.get("description_bullets", [])),
    )

    for attempt in range(2):
        try:
            response = client.messages.create(
                model=MODEL,
                max_tokens=512,
                messages=[{"role": "user", "content": prompt}],
            )
            text = response.content[0].text.strip()
            data = json.loads(text)
            if not REQUIRED_KEYS.issubset(data.keys()):
                raise ValueError(f"Missing required keys: {REQUIRED_KEYS - data.keys()}")
            # Ensure alternative_facility key exists (optional field)
            data.setdefault("alternative_facility", None)
            return data
        except Exception as e:
            print(f"Attempt {attempt + 1} failed for job {job.get('id')}: {e}", file=sys.stderr)
            if attempt == 0:
                time.sleep(0.5)

    return dict(FALLBACK)


def main() -> None:
    with open(JOBS_NEW_FILE) as f:
        jobs = json.load(f)

    if not jobs:
        with open(JOBS_ENRICHED_FILE, "w") as f:
            json.dump([], f)
        print("No new jobs to identify")
        return

    client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from environment

    enriched = []
    for i, job in enumerate(jobs):
        print(f"Identifying facility for job {i + 1}/{len(jobs)}: {job.get('title', '')[:60]}")
        identification = identify_facility(client, job)
        enriched.append({**job, "identification": identification})
        if i < len(jobs) - 1:
            time.sleep(0.5)

    with open(JOBS_ENRICHED_FILE, "w") as f:
        json.dump(enriched, f, indent=2)

    identified = sum(1 for j in enriched if j["identification"]["confidence"] != "none")
    print(f"Identified {identified}/{len(enriched)} facilities")


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run tests and verify they pass**

```bash
cd comphealth-scraper
python -m pytest tests/test_identifier.py -v
```

Expected: all 5 tests pass.

- [ ] **Step 5: Commit**

```bash
git add comphealth-scraper/identifier.py comphealth-scraper/tests/test_identifier.py
git commit -m "feat: add Claude API facility identifier with tests"
```

---

## Task 5: Emailer (`emailer.py`)

**Files:**
- Create: `comphealth-scraper/emailer.py`
- Create: `comphealth-scraper/tests/test_emailer.py`

- [ ] **Step 1: Write the failing tests**

Create `comphealth-scraper/tests/test_emailer.py`:

```python
import os
import pytest
from unittest.mock import MagicMock, patch


def make_enriched_job(**kwargs) -> dict:
    defaults = {
        "id": "job-1",
        "title": "Cardiologist in TX",
        "location": "Austin, TX",
        "specialty": "Cardiology",
        "job_type": "Locum Tenens",
        "url": "https://www.comphealth.com/jobs/job-1",
        "identification": {
            "facility_name": "St. David's Medical Center",
            "facility_type": "Community Hospital",
            "confidence": "high",
            "reasoning": "Only major cardiac center",
            "alternative_facility": "Ascension Seton",
        },
    }
    return {**defaults, **kwargs}


class TestBuildTable:
    def test_returns_no_postings_message_for_empty_list(self):
        import emailer
        html = emailer.build_table([])
        assert "No new job postings" in html

    def test_includes_job_title_in_output(self):
        import emailer
        jobs = [make_enriched_job()]
        html = emailer.build_table(jobs)
        assert "Cardiologist in TX" in html

    def test_includes_facility_name(self):
        import emailer
        jobs = [make_enriched_job()]
        html = emailer.build_table(jobs)
        assert "St. David's Medical Center" in html

    def test_includes_alternative_facility(self):
        import emailer
        jobs = [make_enriched_job()]
        html = emailer.build_table(jobs)
        assert "Ascension Seton" in html

    def test_omits_also_possible_when_alternative_is_none(self):
        import emailer
        job = make_enriched_job()
        job["identification"]["alternative_facility"] = None
        html = emailer.build_table([job])
        assert "Also possible" not in html

    def test_high_confidence_uses_green_background(self):
        import emailer
        jobs = [make_enriched_job()]
        html = emailer.build_table(jobs)
        assert "#d4edda" in html

    def test_unable_to_identify_uses_gray_background(self):
        import emailer
        job = make_enriched_job()
        job["identification"] = {
            "facility_name": "Unable to identify",
            "confidence": "none",
            "reasoning": "",
            "alternative_facility": None,
        }
        html = emailer.build_table([job])
        assert "#e2e3e5" in html

    def test_includes_link_to_job(self):
        import emailer
        jobs = [make_enriched_job()]
        html = emailer.build_table(jobs)
        assert "https://www.comphealth.com/jobs/job-1" in html


class TestBuildSuccessEmail:
    def test_subject_includes_count(self):
        import emailer
        subject, _ = emailer.build_success_email([make_enriched_job()])
        assert "1 new posting" in subject

    def test_subject_no_postings_when_empty(self):
        import emailer
        subject, _ = emailer.build_success_email([])
        assert "No new postings" in subject


class TestBuildFailureEmail:
    def test_subject_includes_warning(self):
        import emailer
        subject, _ = emailer.build_failure_email("Site unreachable")
        assert "Failed" in subject

    def test_body_includes_reason(self):
        import emailer
        _, body = emailer.build_failure_email("Site unreachable")
        assert "Site unreachable" in body


class TestSendEmailGmail:
    def test_sends_via_gmail_smtp(self):
        import emailer
        env = {
            "EMAIL_TRANSPORT": "gmail",
            "GMAIL_USER": "sender@gmail.com",
            "GMAIL_APP_PASSWORD": "app-pass",
            "RECIPIENT_EMAIL": "tyler@connecthealthstaff.com",
        }
        with patch.dict(os.environ, env):
            with patch("smtplib.SMTP") as mock_smtp:
                mock_server = MagicMock()
                mock_smtp.return_value.__enter__ = MagicMock(return_value=mock_server)
                mock_smtp.return_value.__exit__ = MagicMock(return_value=False)
                emailer.send_email("Subject", "<p>body</p>", is_html=True)
                mock_server.sendmail.assert_called_once()


class TestSendEmailSendGrid:
    def test_sends_via_sendgrid(self):
        import emailer
        env = {
            "EMAIL_TRANSPORT": "sendgrid",
            "SENDGRID_API_KEY": "SG.fake",
            "GMAIL_USER": "sender@gmail.com",
            "RECIPIENT_EMAIL": "tyler@connecthealthstaff.com",
        }
        with patch.dict(os.environ, env):
            with patch("sendgrid.SendGridAPIClient") as mock_sg_class:
                mock_sg = MagicMock()
                mock_sg_class.return_value = mock_sg
                emailer.send_email("Subject", "<p>body</p>", is_html=True)
                mock_sg.send.assert_called_once()
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
cd comphealth-scraper
python -m pytest tests/test_emailer.py -v
```

Expected: `ModuleNotFoundError: No module named 'emailer'`

- [ ] **Step 3: Create `comphealth-scraper/emailer.py`**

```python
import json
import os
import smtplib
import sys
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

JOBS_ENRICHED_FILE = Path(__file__).parent / "jobs_enriched.json"

CONFIDENCE_COLORS = {
    "high": "#d4edda",
    "medium": "#fff3cd",
    "low": "#f8d7da",
    "none": "#e2e3e5",
}

_TD = 'style="padding: 8px; border: 1px solid #ddd;"'
_TH = 'style="padding: 8px; border: 1px solid #ddd; text-align: left; background-color: #f2f2f2;"'


def build_table(jobs: list[dict]) -> str:
    if not jobs:
        return "<p>No new job postings today.</p>"

    rows = []
    for job in jobs:
        ident = job.get("identification", {})
        confidence = ident.get("confidence", "none")
        bg = CONFIDENCE_COLORS.get(confidence, CONFIDENCE_COLORS["none"])

        facility_name = ident.get("facility_name", "Unable to identify")
        facility_cell = f"<strong>{facility_name}</strong>"
        if confidence not in ("none", ""):
            facility_cell += f" ({confidence.capitalize()})"
        alt = ident.get("alternative_facility")
        if alt:
            facility_cell += f"<br><small><em>Also possible: {alt}</em></small>"

        url = job.get("url", "#")
        rows.append(
            f'<tr style="background-color: {bg};">'
            f"<td {_TD}>{job.get('title', '')}</td>"
            f"<td {_TD}>{job.get('location', '')}</td>"
            f"<td {_TD}>{job.get('specialty', '')}</td>"
            f"<td {_TD}>{job.get('job_type', '')}</td>"
            f"<td {_TD}>{facility_cell}</td>"
            f'<td {_TD}><a href="{url}">View</a></td>'
            "</tr>"
        )

    header = (
        '<table style="border-collapse: collapse; width: 100%; font-family: Arial, sans-serif; font-size: 13px;">'
        "<thead><tr>"
        f"<th {_TH}>Job Title</th>"
        f"<th {_TH}>Location</th>"
        f"<th {_TH}>Specialty</th>"
        f"<th {_TH}>Type</th>"
        f"<th {_TH}>Likely Facility</th>"
        f"<th {_TH}>Link</th>"
        "</tr></thead><tbody>"
    )
    return header + "".join(rows) + "</tbody></table>"


def build_success_email(jobs: list[dict]) -> tuple[str, str]:
    date = datetime.today().strftime("%Y-%m-%d")
    count = len(jobs)
    if count == 0:
        subject = f"CompHealth New Jobs — {date} (No new postings)"
        body = f"<p style='font-family:Arial,sans-serif;'>No new job postings found on {date}.</p>"
    else:
        subject = f"CompHealth New Jobs — {date} ({count} new posting{'s' if count != 1 else ''})"
        body = (
            f"<div style='font-family:Arial,sans-serif;'>"
            f"<h2>CompHealth New Jobs — {date}</h2>"
            f"<p>{count} new posting{'s' if count != 1 else ''} since last run</p>"
            f"{build_table(jobs)}"
            f"</div>"
        )
    return subject, body


def build_failure_email(reason: str) -> tuple[str, str]:
    date = datetime.today().strftime("%Y-%m-%d")
    subject = f"⚠️ CompHealth Scraper Failed — {date}"
    body = (
        f"CompHealth scraper failed on {date}.\n\n"
        f"Error: {reason}\n\n"
        "Check GitHub Actions logs for full details.\n"
        "The scraper will retry on the next scheduled run."
    )
    return subject, body


def send_email(subject: str, body: str, is_html: bool = True) -> None:
    transport = os.environ.get("EMAIL_TRANSPORT", "gmail").lower()
    recipient = os.environ["RECIPIENT_EMAIL"]

    if transport == "sendgrid":
        _send_sendgrid(subject, body, recipient, is_html)
    else:
        _send_gmail(subject, body, recipient, is_html)


def _send_gmail(subject: str, body: str, recipient: str, is_html: bool) -> None:
    sender = os.environ["GMAIL_USER"]
    password = os.environ["GMAIL_APP_PASSWORD"]

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = recipient
    msg.attach(MIMEText(body, "html" if is_html else "plain"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, recipient, msg.as_string())


def _send_sendgrid(subject: str, body: str, recipient: str, is_html: bool) -> None:
    import sendgrid
    from sendgrid.helpers.mail import Mail

    sender = os.environ.get("GMAIL_USER", "noreply@connecthealthstaff.com")
    message = Mail(
        from_email=sender,
        to_emails=recipient,
        subject=subject,
        html_content=body if is_html else None,
        plain_text_content=None if is_html else body,
    )
    sg = sendgrid.SendGridAPIClient(os.environ["SENDGRID_API_KEY"])
    sg.send(message)


def main() -> None:
    failure_mode = "--failure" in sys.argv

    if failure_mode:
        reason = os.environ.get("FAILURE_REASON", "Unknown error — check GitHub Actions logs")
        subject, body = build_failure_email(reason)
        send_email(subject, body, is_html=False)
        print(f"Failure notification sent: {subject}")
        return

    with open(JOBS_ENRICHED_FILE) as f:
        jobs = json.load(f)

    subject, body = build_success_email(jobs)
    send_email(subject, body, is_html=True)
    print(f"Email sent: {subject}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run tests and verify they pass**

```bash
cd comphealth-scraper
python -m pytest tests/test_emailer.py -v
```

Expected: all 12 tests pass.

- [ ] **Step 5: Run the full test suite**

```bash
cd comphealth-scraper
python -m pytest tests/ -v
```

Expected: all tests pass.

- [ ] **Step 6: Commit**

```bash
git add comphealth-scraper/emailer.py comphealth-scraper/tests/test_emailer.py
git commit -m "feat: add emailer with Gmail/SendGrid support and tests"
```

---

## Task 6: GitHub Actions Workflow

**Files:**
- Create: `.github/workflows/daily-scrape.yml`

- [ ] **Step 1: Create `.github/workflows/daily-scrape.yml`**

```yaml
name: CompHealth Daily Job Scraper

on:
  schedule:
    - cron: '0 12 * * 1-5'   # ~7 AM ET weekdays (7 AM EST / 8 AM EDT)
  workflow_dispatch:            # allow manual runs from GitHub UI

jobs:
  scrape:
    runs-on: ubuntu-latest
    timeout-minutes: 30
    concurrency:
      group: daily-scrape
      cancel-in-progress: false   # skip new trigger if already running

    permissions:
      contents: write   # required to commit state.json

    defaults:
      run:
        working-directory: comphealth-scraper

    steps:
      - name: Checkout repo
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Install Playwright browsers
        run: playwright install chromium

      - name: Scrape new jobs
        run: python scraper.py

      - name: Identify facilities
        run: python identifier.py
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}

      - name: Send email report
        run: python emailer.py
        env:
          EMAIL_TRANSPORT: ${{ secrets.EMAIL_TRANSPORT }}
          RECIPIENT_EMAIL: ${{ secrets.RECIPIENT_EMAIL }}
          GMAIL_USER: ${{ secrets.GMAIL_USER }}
          GMAIL_APP_PASSWORD: ${{ secrets.GMAIL_APP_PASSWORD }}
          SENDGRID_API_KEY: ${{ secrets.SENDGRID_API_KEY }}

      - name: Commit updated state
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add state.json
          git diff --cached --quiet || git commit -m "chore: update seen job IDs [skip ci]"
          git push

      - name: Send failure notification
        if: failure()
        run: python emailer.py --failure
        env:
          EMAIL_TRANSPORT: ${{ secrets.EMAIL_TRANSPORT }}
          RECIPIENT_EMAIL: ${{ secrets.RECIPIENT_EMAIL }}
          GMAIL_USER: ${{ secrets.GMAIL_USER }}
          GMAIL_APP_PASSWORD: ${{ secrets.GMAIL_APP_PASSWORD }}
          SENDGRID_API_KEY: ${{ secrets.SENDGRID_API_KEY }}
          FAILURE_REASON: "A step failed — check the GitHub Actions run log for details."
```

- [ ] **Step 2: Commit the workflow**

```bash
git add .github/workflows/daily-scrape.yml
git commit -m "feat: add GitHub Actions daily scrape workflow"
```

---

## Task 7: GitHub Setup & Secrets Configuration

**Prerequisite:** A GitHub account and repo. Push the code to GitHub before this task.

- [ ] **Step 1: Create the GitHub repository and push**

```bash
# From the repo root
git remote add origin https://github.com/YOUR_USERNAME/comphealth-scraper.git
git push -u origin main
```

- [ ] **Step 2: Configure repository secrets**

Go to: `https://github.com/YOUR_USERNAME/comphealth-scraper/settings/secrets/actions`

Add the following secrets:

| Secret Name | Value |
|---|---|
| `ANTHROPIC_API_KEY` | Your Anthropic API key from console.anthropic.com |
| `EMAIL_TRANSPORT` | `gmail` (or `sendgrid` if Workspace blocks app passwords) |
| `RECIPIENT_EMAIL` | `tyler@connecthealthstaff.com` |
| `GMAIL_USER` | The Gmail address to send from |
| `GMAIL_APP_PASSWORD` | Gmail app password (from myaccount.google.com → Security → 2-Step → App passwords) |
| `SENDGRID_API_KEY` | Only required if `EMAIL_TRANSPORT=sendgrid` |

**Gmail app password note:** If connecthealthstaff.com is a Google Workspace account and app passwords are blocked by admin policy, use SendGrid instead. Sign up at sendgrid.com (free tier: 100 emails/day) and set `EMAIL_TRANSPORT=sendgrid`.

- [ ] **Step 3: Enable Actions write permissions**

Go to: `https://github.com/YOUR_USERNAME/comphealth-scraper/settings/actions`

Under "Workflow permissions", select **"Read and write permissions"**. This allows the workflow to commit `state.json`.

- [ ] **Step 4: Trigger a manual test run**

Go to: `https://github.com/YOUR_USERNAME/comphealth-scraper/actions`

Click **"CompHealth Daily Job Scraper"** → **"Run workflow"** → **"Run workflow"**.

Monitor the run. Verify:
- Scraper step completes and shows job count
- Identifier step completes
- Email arrives at tyler@connecthealthstaff.com
- A commit to `state.json` appears in the repo

- [ ] **Step 5: Verify the email**

Open the email. Check:
- Subject includes today's date and job count
- Table is rendered with color-coded rows
- Job titles, locations, and facility names are populated
- "View" links open the correct CompHealth job pages

---

## Final Checklist

- [ ] All unit tests pass: `cd comphealth-scraper && python -m pytest tests/ -v`
- [ ] Manual scrape produces valid `jobs_new.json`
- [ ] Manual identify produces valid `jobs_enriched.json` with facility names
- [ ] Test email sent and received at tyler@connecthealthstaff.com
- [ ] GitHub Actions workflow ran successfully end-to-end
- [ ] `state.json` committed back to repo after run
- [ ] Second manual run produces no duplicate jobs from the first run
