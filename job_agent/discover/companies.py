from typing import Iterable, List, Optional


DEFAULT_COMPANIES = [
    "airbnb",
    "stripe",
    "databricks",
    "uber",
    "spotify",
    "adobe",
    "meta",
    "google",
]


def get_company_list(
    user_companies: Optional[Iterable[str]] = None,
) -> List[str]:
    """
    Returns the final list of companies to ingest jobs from.

    - Starts with a default curated list
    - Optionally merges user-provided companies
    """
    companies = set(DEFAULT_COMPANIES)

    if user_companies:
        companies.update(c.strip().lower() for c in user_companies)

    return sorted(companies)
