# rank/signals.py
from job_agent.models.job import JobPosting
from job_agent.models.profile import UserProfile

def extract_signals(job: JobPosting, profile: UserProfile) -> dict:
    text = f"{job.title} {job.description}".lower()

    signals = {}

    # Skill overlap
    skill_hits = sum(1 for skill in profile.core_skills if skill in text)
    signals["skill_overlap"] = min(skill_hits / max(len(profile.core_skills), 1), 1.0)

    # ML depth
    ml_depth_terms = ["train", "model", "evaluate", "experiment", "research"]
    depth_hits = sum(1 for t in ml_depth_terms if t in text)
    signals["ml_depth"] = min(depth_hits / len(ml_depth_terms), 1.0)

    # Ownership language
    ownership_terms = ["own", "design", "lead", "build"]
    ownership_hits = sum(1 for t in ownership_terms if t in text)
    signals["ownership"] = min(ownership_hits / len(ownership_terms), 1.0)

    return signals
