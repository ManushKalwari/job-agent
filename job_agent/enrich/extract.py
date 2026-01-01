# job_agent/enrich/extract.py

from bs4 import BeautifulSoup

def extract_job_text(html: str) -> str:
    """
    Extract readable job description text from HTML.
    """
    soup = BeautifulSoup(html, "html.parser")

    # Greenhouse pages are usually clean:
    main = soup.find("div", {"class": "content"})
    if not main:
        main = soup.body

    text = main.get_text(separator="\n", strip=True)
    return text
