# backend/api/schemas.py

from pydantic import BaseModel
from typing import List


from pydantic import BaseModel
from typing import List


# ---------- DISCOVERY ----------

class JobDiscoverRequest(BaseModel):
    target_roles: List[str]
    core_skills: List[str]
    location: List[str]


class JobDiscoverResult(BaseModel):
    job_id: str
    title: str
    company: str
    location: str
    apply_url: str
    poe: float


# ---------- COVER LETTER ----------

class CoverLetterRequest(BaseModel):
    job_ids: List[str]
    resume_text: str


class CoverLetterResult(BaseModel):
    filename: str
