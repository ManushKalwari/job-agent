# job_agent/rank/text.py
from job_agent.models.job import JobPosting
from job_agent.models.profile import UserProfile

def job_text(job: JobPosting) -> str:
    """
    Canonical text representation of a job for retrieval/ranking.
    """
    desc = job.description or ""
    return (
        f"Title: {job.title}\n"
        f"Company: {job.company}\n"
        f"Location: {job.location}\n"
        f"{desc}"
    )

def profile_query(profile: UserProfile) -> str:
    """
    Canonical text representation of user intent.
    """
    roles = ", ".join(profile.target_roles)
    skills = ", ".join(profile.core_skills)

    return (
        f"Target roles: {roles}. "
        f"Core skills: {skills}."
    )
