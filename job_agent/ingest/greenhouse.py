# ingest/greenhouse.py

import requests
from typing import List, Dict

GREENHOUSE_API = "https://boards-api.greenhouse.io/v1/boards"

def fetch_jobs(company_slug: str) -> List[Dict]:
    """
    Fetch raw job postings from Greenhouse.
    Returns list of raw job dicts.
    """
    url = f"{GREENHOUSE_API}/{company_slug}/jobs"
    print(f"[ingest] fetching jobs from {url}")
    resp = requests.get(url, timeout=10)
    print("[ingest] response received")
    resp.raise_for_status()
    data = resp.json()
    print(f"[ingest] {len(data.get('jobs', []))} jobs found")
    return data.get("jobs", [])
