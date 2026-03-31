"""
scraper.py — Scrape new CompHealth job postings for today.

Writes jobs_new.json (new unseen jobs) and updates state.json.

Exit codes:
  0 — success (full or partial)
  1 — fatal failure (site unreachable, blocked, sanity check failed)
"""
import asyncio
import json
import random
import re
import sys
from pathlib import Path
from playwright.async_api import async_playwright, Page

import state as state_module

JOBS_NEW_FILE = Path(__file__).parent / "jobs_new.json"
BASE_URL = "https://www.comphealth.com"
JOBS_URL = f"{BASE_URL}/jobs?datePosted=today&sort=newest"
MIN_TOTAL_JOBS = 100
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
)


async def get_total_job_count(page: Page) -> int:
    """Parse total job count from h1, e.g. '10611 All CompHealth jobs'."""
    try:
        text = await page.locator("h1").first.text_content(timeout=5000) or ""
        match = re.search(r"[\d,]+", text)
        if match:
            return int(match.group().replace(",", ""))
    except Exception:
        pass
    return 0


async def extract_job_from_card(card):
    """Extract all available fields from a single .job-card element."""
    try:
        # Job URL and ID
        href = await card.locator("a[href^='/job/']").first.get_attribute("href", timeout=3000)
        if not href:
            return None
        job_id = href.rstrip("/").split("/")[-1]

        # Title (first h4 in card)
        title = await _text(card.locator("h4").first)

        # h6 tags carry: date tag, compensation, job type, location (in that order)
        h6s = card.locator("h6.job-info-tag")
        compensation = ""
        job_type = ""
        location_raw = ""
        label_tags_seen = 0

        for i in range(await h6s.count()):
            h6 = h6s.nth(i)
            cls = await h6.get_attribute("class") or ""
            text = re.sub(r"\s+", " ", await _text(h6)).strip()

            if "bg-primary" in cls:
                pass  # "Posted today" tag — skip
            elif "chg-tooltip-action" in cls:
                # Compensation — strip tooltip text inside <span>
                try:
                    span_text = await h6.locator(".chg-tooltip").text_content(timeout=2000) or ""
                    compensation = text.replace(span_text.strip(), "").strip()
                except Exception:
                    compensation = text
            elif "label-12" in cls:
                if label_tags_seen == 0:
                    job_type = text
                else:
                    location_raw = text
                label_tags_seen += 1

        # Parse city/state from location string e.g. "Wolfeboro, New Hampshire"
        city, state = "", ""
        if "," in location_raw:
            parts = location_raw.split(",", 1)
            city = parts[0].strip()
            state = parts[1].strip()

        # Description bullets
        bullets = []
        bullet_els = card.locator("ul li")
        for i in range(min(await bullet_els.count(), 8)):
            t = await _text(bullet_els.nth(i))
            if t:
                bullets.append(t)

        full_url = href if href.startswith("http") else BASE_URL + href

        return {
            "id": job_id,
            "title": title,
            "city": city,
            "state": state,
            "location": location_raw,
            "job_type": job_type,
            "compensation": compensation,
            "description_bullets": bullets,
            "url": full_url,
        }
    except Exception as e:
        print(f"Warning: failed to extract job card: {e}", file=sys.stderr)
        return None


async def _text(locator) -> str:
    """Get stripped text from a locator, returning '' on failure."""
    try:
        t = await locator.text_content(timeout=3000)
        return (t or "").strip()
    except Exception:
        return ""


async def scrape_all_jobs() -> tuple[list, bool]:
    """
    Scrape all jobs posted today.
    Returns (jobs, is_complete) where is_complete=False means pagination
    failed mid-way (partial results are still valid and should be saved).
    """
    jobs = []
    is_complete = True

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(user_agent=USER_AGENT)

        try:
            await page.goto(JOBS_URL, wait_until="domcontentloaded", timeout=60000)
            await asyncio.sleep(2)

            # Sanity check: verify site is up and working
            total = await get_total_job_count(page)
            if total < MIN_TOTAL_JOBS:
                raise RuntimeError(
                    f"Sanity check failed: only {total} total jobs visible "
                    f"(expected >= {MIN_TOTAL_JOBS}). Site may be blocked or changed."
                )
            print(f"Site OK — {total:,} total jobs. Scraping today's postings...", file=sys.stderr)

            page_num = 1
            while True:
                cards = page.locator(".job-card")
                card_count = await cards.count()

                # Stop if no cards have "Posted today" tag — we've moved past today's jobs
                today_count = await page.locator("h6.job-info-tag.bold.bg-primary").count()
                print(f"  Page {page_num}: {card_count} cards, {today_count} posted today", file=sys.stderr)
                if today_count == 0:
                    print("  No more 'Posted today' cards — stopping pagination", file=sys.stderr)
                    break

                for i in range(card_count):
                    job = await extract_job_from_card(cards.nth(i))
                    if job:
                        jobs.append(job)

                # Check for enabled next-page button
                next_btn = page.locator("[aria-label*='Next']").first
                try:
                    if await next_btn.count() == 0 or not await next_btn.is_enabled(timeout=3000):
                        break
                except Exception:
                    break

                try:
                    await next_btn.click()
                    await page.wait_for_load_state("domcontentloaded", timeout=20000)
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
    seen_ids = state_module.get_seen_ids()

    try:
        all_jobs, is_complete = asyncio.run(scrape_all_jobs())
    except RuntimeError as e:
        # Sanity check failure or hard site error
        print(f"SCRAPER_FATAL: {e}", file=sys.stderr)
        sys.exit(1)

    # Deduplicate against state (post-collection, all pages gathered first)
    new_jobs = [j for j in all_jobs if j["id"] not in seen_ids]

    # Write new jobs to temp file for identifier.py
    with open(JOBS_NEW_FILE, "w") as f:
        json.dump(new_jobs, f, indent=2)

    # Persist new IDs to state (even on partial scrape)
    state_module.add_jobs(new_jobs)

    status = "COMPLETE" if is_complete else "PARTIAL (pagination failed)"
    print(f"Scrape {status}: {len(new_jobs)} new jobs out of {len(all_jobs)} scraped")

    if not is_complete:
        # Signal to workflow that results may be incomplete
        print("SCRAPER_PARTIAL: results may be incomplete", file=sys.stderr)


if __name__ == "__main__":
    main()
