# models/profile.py
from dataclasses import dataclass
from typing import List

@dataclass
class UserProfile:
    target_roles: List[str]
    core_skills: List[str]
    exclude_keywords: List[str]
