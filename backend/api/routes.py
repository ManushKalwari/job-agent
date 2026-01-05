# backend/api/routes.py

from fastapi import APIRouter, UploadFile, File, Form

from .schemas import (
    JobDiscoverRequest,
    JobDiscoverResult,
)

from backend.services.discover import discover_jobs
from backend.services.cover_letter import generate_cover_letter

router = APIRouter()


# -------------------------
# Discover jobs
# -------------------------
@router.post("/jobs/discover", response_model=list[JobDiscoverResult])
def discover(profile: JobDiscoverRequest):
    return discover_jobs(profile)


# -------------------------
# Generate cover letters
# -------------------------
@router.post("/jobs/cover-letter")
def cover_letter(
    resume: UploadFile = File(...),
    job_ids: list[str] = Form(...)
):
    return generate_cover_letter(
        resume_file=resume,
        job_ids=job_ids
    )
