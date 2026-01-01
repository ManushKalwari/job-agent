import requests
from bs4 import BeautifulSoup

def fetch_job_page(url: str) -> str:
    """
    Fetch raw HTML from a job apply page.
    """
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    return resp.text