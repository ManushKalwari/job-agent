# ingest/parser.py

import re
from datetime import datetime
from typing import Optional
from job_agent.models.job import JobPosting

_HTML_TAG_RE = re.compile(r"<[^>]+>")

def _strip_html(text: str) -> str:
    if not text:
        return ""
    text = _HTML_TAG_RE.sub("", text)
    return text.strip()

def _parse_date(date_str: Optional[str]) -> Optional[datetime.date]:
    if not date_str:
        return None
    try:
        return datetime.fromisoformat(date_str.replace("Z", "")).date()
    except Exception:
        return None

def parse_greenhouse_job(raw_job: dict, company: str) -> JobPosting:
    """
    Convert Greenhouse job JSON → JobPosting
    Defensive by default.
    """
    job_id = str(raw_job.get("id"))

    title = raw_job.get("title", "").strip()

    location = ""
    loc = raw_job.get("location")
    if isinstance(loc, dict):
        location = loc.get("name", "").strip()

    description = _strip_html(raw_job.get("content", ""))

    apply_url = raw_job.get("absolute_url", "")

    posted_date = _parse_date(raw_job.get("updated_at"))

    return JobPosting(
        job_id=job_id,
        company=company,
        title=title,
        location=location,
        description=description,
        apply_url=apply_url,
        posted_date=posted_date,
        source="greenhouse",
    )
