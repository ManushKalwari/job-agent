# ingest/greenhouse.py

import requests
from typing import List, Dict

GREENHOUSE_API = "https://boards-api.greenhouse.io/v1/boards"

def fetch_jobs(company_slug: str) -> List[Dict]:
    """
    Fetch raw job postings from a Greenhouse board.
    Returns an empty list if the board does not exist or is unreachable.
    """
    url = f"{GREENHOUSE_API}/{company_slug}/jobs"
    print(f"[ingest] fetching jobs from {url}")

    try:
        resp = requests.get(url, timeout=10)

        if resp.status_code == 404:
            print(f"[ingest] no Greenhouse board found for '{company_slug}', skipping")
            return []

        resp.raise_for_status()

        data = resp.json()
        jobs = data.get("jobs", [])
        print(f"[ingest] {len(jobs)} jobs found for '{company_slug}'")
        return jobs

    except requests.exceptions.RequestException as e:
        print(f"[ingest] failed to fetch jobs for '{company_slug}': {e}")
        return []