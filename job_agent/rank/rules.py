# rank/rules.py

import re

from job_agent.models.job import JobPosting
from job_agent.models.profile import UserProfile

import re
from job_agent.models.job import JobPosting
from job_agent.models.profile import UserProfile
from job_agent.rank.location import is_us_location



def passes_rules(job: JobPosting, profile: UserProfile) -> bool:
    # location hard filter
    if profile.location:
        if "us" in [loc.lower() for loc in profile.location]:
            if not is_us_location(job.location or ""):
                return False

    return True