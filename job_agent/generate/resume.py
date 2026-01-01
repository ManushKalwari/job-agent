# generate/resume.py
from pypdf import PdfReader
from pathlib import Path


def parse_resume_pdf(pdf_path: str | Path) -> str:
    """
    Extract text from a PDF resume.
    Returns clean plain text.
    """
    reader = PdfReader(str(pdf_path))
    pages = []

    for page in reader.pages:
        text = page.extract_text()
        if text:
            pages.append(text)

    full_text = "\n".join(pages)

    # light cleanup
    full_text = full_text.replace("\xa0", " ")
    full_text = "\n".join(
        line.strip() for line in full_text.splitlines() if line.strip()
    )

    return full_text
