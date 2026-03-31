# CompHealth Daily Job Scraper — Design Spec

**Date:** 2026-03-31
**Author:** Tyler Meeks
**Status:** Approved

---

## Overview

A daily automated system that scrapes new job postings from comphealth.com, uses the Claude API to identify the most likely US healthcare facility for each anonymized posting, and emails a formatted report to tyler@connecthealthstaff.com every weekday morning at approximately 7:00 AM ET.

CompHealth deliberately anonymizes facility/client names in job listings (e.g., "A Facility in Pennsylvania"). This system uses AI reasoning to reverse-engineer the likely facility from available clues: city, state, specialty, job type, compensation range, and description details.

**Email timing:** The daily email captures jobs detected as new since the previous run, based on job ID. Jobs posted that same morning before the scrape runs are included.

**"New" job definition:** A job is new if its ID is not in `state.json`. Re-posts with new IDs count as new. Updated listings that keep their original ID are not re-sent. Semantic duplicate detection is out of scope.

---

## Architecture

```
comphealth-scraper/
├── .github/
│   └── workflows/
│       └── daily-scrape.yml
├── scraper.py          # Fetches new jobs from comphealth.com via Playwright
├── identifier.py       # Claude API facility identification
├── emailer.py          # HTML email formatter + sender (Gmail or SendGrid)
├── state.json          # Persisted set of recently-seen job IDs
└── requirements.txt    # anthropic, playwright, sendgrid, jinja2
```

### Data Flow

```
GitHub Actions (~7AM ET)
  → scraper.py fetches today's jobs (Playwright, headless Chromium)
  → compares against state.json, extracts unseen jobs
  → identifier.py sends each new job to Claude API
  → emailer.py formats HTML table + sends email
  → GitHub Actions commits updated state.json back to repo
```

---

## Component 1: Scraper (`scraper.py`)

**Approach:** Playwright (headless Chromium). CompHealth renders via JavaScript and will not respond to plain HTTP requests.

**Target:** comphealth.com/jobs filtered to jobs posted today, sorted newest first. The exact URL parameters are confirmed during implementation. If query parameters don't work, Playwright interacts with on-page filters directly (click "Today" date filter, sort by newest).

**Sanity check:** After loading the page, verify the total job count visible is at least 100. If fewer than 100 total listings are visible, treat this as a likely scraper failure (site structure changed or blocked), log the error, send a failure notification, and abort without updating state.

**First-run behavior:** If `state.json` does not exist, create an empty one (`[]`) and scrape only today's jobs. All of today's jobs will appear in the first email.

**Fields extracted per job:**
- Job ID (from URL slug or data attribute — confirmed during implementation)
- Job title
- City, State
- Specialty
- Job type (Locum Tenens / Permanent / Travel / Telehealth)
- Compensation range
- Description bullet points
- Job URL

**Pagination:** Collect all pages of today's results before any deduplication. Termination: no more pages. Deduplication against `state.json` happens post-collection.

**Bot mitigation:** Set a realistic `User-Agent` header. Add random 1–3 second delays between page loads.

**State file format:**
```json
[
  {"id": "job-12345", "seen_date": "2026-03-31"},
  {"id": "job-12346", "seen_date": "2026-03-31"}
]
```
After each completed run, new IDs are appended, the array is deduplicated by `id`, and entries with `seen_date` older than 60 days are pruned.

**Partial scrape:** If pagination fails mid-way, the jobs collected so far are treated as the result set. Their IDs are written to `state.json` so they don't reappear tomorrow. The email notes the results may be incomplete.

**Timeout handling:** If the GitHub Actions job is killed by the 30-minute timeout, the state is not updated (the commit step never runs). The next run will re-scrape fresh. This is distinct from a detected pagination error — timeout is an external kill, not a caught exception.

---

## Component 2: Facility Identifier (`identifier.py`)

**Model:** `claude-haiku-4-5-20251001` (verified against Anthropic's current model list as of 2026-03-31)

**Cost estimate:** 50–100 new jobs/day → ~$0.04–$0.08/day.

**Prompt:** Sends all job fields and requests structured JSON:

```json
{
  "facility_name": "Regional Medical Center of San Jose",
  "facility_type": "Community Hospital",
  "confidence": "high | medium | low",
  "reasoning": "Only Level II trauma center in San Jose with locum cardiology openings at this rate",
  "alternative_facility": "Good Samaritan Hospital San Jose"
}
```

`alternative_facility` is captured and included in the email as a secondary "Also possible:" line below the main facility name. It is not a required field — if absent or null, that line is omitted.

**Confidence levels:**
- `high` — strong match on multiple specific details
- `medium` — plausible match, some ambiguity
- `low` — city/state only, multiple facilities possible

**Rate limiting:** 0.5-second delay between calls.

**Response validation:** Parse as JSON, validate required keys (`facility_name`, `confidence`, `reasoning`). On failure, retry once. On second failure, mark as `"Unable to identify"` / `confidence: "none"`. Jobs are never dropped.

---

## Component 3: Emailer (`emailer.py`)

### Success Email

**Subject:** `CompHealth New Jobs — 2026-03-31 (47 new postings)`

**Body:** HTML table with row background colors indicating confidence:

| Job Title | Location | Specialty | Type | Likely Facility | Link |
|---|---|---|---|---|---|
| Cardiologist in TX | Austin, TX | Cardiology | Locum | **St. David's Medical Center** (High) | View |
| Hospitalist in IL | Chicago, IL | Hospitalist | Permanent | **Northwestern Memorial** (Medium)<br>*Also possible: Rush University Medical Center* | View |
| PA Needed in PA | Philadelphia, PA | Gen. Surgery | Locum | Unable to identify | View |

**Row background colors (applied via inline CSS):**
- `#d4edda` (green) = High confidence
- `#fff3cd` (yellow) = Medium confidence
- `#f8d7da` (red) = Low confidence
- `#e2e3e5` (gray) = Unable to identify

### Failure Notification Email

Sent for: site unreachable, CAPTCHA, state commit failure, or any unhandled exception.

**Subject:** `⚠️ CompHealth Scraper Failed — 2026-03-31`

**Body:** Plain text. Includes:
- Error type (e.g., "Site unreachable", "state.json commit failed")
- Error message / stack trace excerpt
- Whether partial results were emailed before the failure

### Transport

**Default: Gmail SMTP** (port 587, STARTTLS). Requires `GMAIL_USER` + `GMAIL_APP_PASSWORD` secrets.

**Fallback: SendGrid**. When `EMAIL_TRANSPORT=sendgrid`, uses `SENDGRID_API_KEY`. The emailer does **not** automatically fall back from Gmail to SendGrid — transport is selected by the `EMAIL_TRANSPORT` variable at deploy time. `SENDGRID_API_KEY` only needs to be set if using SendGrid transport.

**Note:** connecthealthstaff.com is a Google Workspace domain. If the admin policy blocks app passwords, set `EMAIL_TRANSPORT=sendgrid` and provision a SendGrid API key.

---

## Component 4: Scheduler (GitHub Actions)

**Workflow file:** `.github/workflows/daily-scrape.yml`

```yaml
on:
  schedule:
    - cron: '0 12 * * 1-5'   # ~7 AM ET weekdays
  workflow_dispatch:           # manual trigger from GitHub UI

jobs:
  scrape:
    runs-on: ubuntu-latest
    timeout-minutes: 30
    concurrency:
      group: daily-scrape
      cancel-in-progress: false  # skip new trigger if run already in progress
    permissions:
      contents: write            # required for state.json commit
```

**Git credentials:** The workflow uses the built-in `GITHUB_TOKEN` (available automatically in all Actions runs) with `contents: write` permission to commit `state.json`. No PAT required. The commit is made with:
```yaml
- run: |
    git config user.name "github-actions[bot]"
    git config user.email "github-actions[bot]@users.noreply.github.com"
    git add state.json
    git diff --cached --quiet || git commit -m "chore: update seen job IDs [skip ci]"
    git push
```
`[skip ci]` in the commit message prevents the push from triggering another workflow run.

**Playwright install:**
```yaml
- run: pip install -r requirements.txt
- run: playwright install chromium
```

**Timezone:** `0 12 * * 1-5` = 7 AM EST (Nov–Mar) and 8 AM EDT (Mar–Nov). To lock at 7 AM ET year-round:
- Each **March** (spring forward): change to `0 11 * * 1-5`
- Each **November** (fall back): change back to `0 12 * * 1-5`

**Secrets required:**
| Secret | Required when |
|---|---|
| `ANTHROPIC_API_KEY` | Always |
| `GMAIL_USER` | `EMAIL_TRANSPORT=gmail` |
| `GMAIL_APP_PASSWORD` | `EMAIL_TRANSPORT=gmail` |
| `SENDGRID_API_KEY` | `EMAIL_TRANSPORT=sendgrid` |
| `EMAIL_TRANSPORT` | Always (`gmail` or `sendgrid`) |
| `RECIPIENT_EMAIL` | Always (set to `tyler@connecthealthstaff.com`) |

---

## Error Handling

| Scenario | Behavior |
|---|---|
| comphealth.com unreachable / CAPTCHA | Send failure notification; do not update state.json |
| Sanity check fails (<100 total jobs visible) | Send failure notification; abort; do not update state.json |
| Claude API down or rate limited | Mark affected jobs "Unable to identify"; complete email send |
| Claude returns invalid/incomplete JSON | Retry once; on second failure, mark "Unable to identify" |
| Gmail SMTP failure | Log to Actions output; no automatic retry (try again next day) |
| No new jobs today | Send "No new postings today" success email |
| Partial scrape (pagination exception) | Send email with jobs collected; note incomplete; commit partial IDs to state |
| Run timeout (killed at 30 min) | State not updated; next run scrapes fresh |
| state.json commit failure | Log error; send failure notification |

---

## Out of Scope

- Matching against a custom client list
- Weekend scheduling (change `1-5` to `*` in cron for daily)
- Historical data beyond 60-day deduplication window
- Web dashboard or UI
- Accuracy validation / ground-truth evaluation

---

## Success Criteria

- Runs reliably every weekday with no manual intervention
- Email arrives before 9 AM ET with all new postings since the previous run
- Zero duplicate job postings across daily emails
- Jobs where facility cannot be identified are marked rather than omitted
- All failure scenarios produce a notification email rather than silent failure
