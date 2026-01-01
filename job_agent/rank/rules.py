# rank/rules.py

import re

from job_agent.models.job import JobPosting
from job_agent.models.profile import UserProfile

import re
from job_agent.models.job import JobPosting
from job_agent.models.profile import UserProfile

def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()



def role_to_pattern(role: str) -> str:
    """
    Convert a role like 'ML Engineer' or 'UI/UX Designer'
    into a flexible regex pattern.
    """
    role = normalize(role)
    tokens = role.split()
    return r"\b" + r"\s*".join(tokens) + r"\b"




def passes_rules(job: JobPosting, profile: UserProfile) -> bool:
    text = f"{job.title} {job.description}".lower()

    # hard exclusions only
    for bad in profile.exclude_keywords:
        if bad and bad.lower() in text:
            return False

    # example: location constraint (optional)
    # if profile.locations and job.location not in profile.locations:
    #     return False

    return True
