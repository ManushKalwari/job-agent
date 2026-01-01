from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass
class JobPosting:
    job_id: str
    company: str
    title: str
    location: str
    description: str
    apply_url: str
    posted_date: Optional[date]
    source: str