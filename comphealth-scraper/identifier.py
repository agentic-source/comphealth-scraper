"""
identifier.py — Identify the most likely US healthcare facility for each job.

Reads jobs_new.json, calls Claude API per job, writes jobs_enriched.json.
"""
import json
import sys
import time
from pathlib import Path

import anthropic

JOBS_NEW_FILE = Path(__file__).parent / "jobs_new.json"
JOBS_ENRICHED_FILE = Path(__file__).parent / "jobs_enriched.json"
MODEL = "claude-haiku-4-5-20251001"
REQUIRED_KEYS = {"facility_name", "confidence", "reasoning"}
FALLBACK = {
    "facility_name": "Unable to identify",
    "facility_type": "",
    "confidence": "none",
    "reasoning": "",
    "alternative_facility": None,
}

USER_PROMPT_TEMPLATE = """Identify the most likely US healthcare facility for this CompHealth job posting.
CompHealth anonymizes facility names, but you can infer the facility from location, specialty, compensation, and description details.

Job details:
Title: {title}
Location: {city}, {state}
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


def identify_facility(client, job: dict) -> dict:
    """
    Call Claude to identify the most likely facility for a job posting.
    Retries once on parse/validation failure. Returns FALLBACK on second failure.
    """
    prompt = USER_PROMPT_TEMPLATE.format(
        title=job.get("title", ""),
        city=job.get("city", ""),
        state=job.get("state", ""),
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
            data.setdefault("alternative_facility", None)
            return data
        except Exception as e:
            print(f"  Attempt {attempt + 1} failed for {job.get('id')}: {e}", file=sys.stderr)
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
        print(f"[{i+1}/{len(jobs)}] {job.get('title', '')[:70]}")
        identification = identify_facility(client, job)
        enriched.append({**job, "identification": identification})
        if i < len(jobs) - 1:
            time.sleep(0.5)

    with open(JOBS_ENRICHED_FILE, "w") as f:
        json.dump(enriched, f, indent=2)

    identified = sum(1 for j in enriched if j["identification"]["confidence"] != "none")
    print(f"Done: identified {identified}/{len(enriched)} facilities")


if __name__ == "__main__":
    main()
