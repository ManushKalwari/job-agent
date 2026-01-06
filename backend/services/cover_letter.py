# backend/services/cover_letter.py

from typing import List
from tempfile import NamedTemporaryFile
import os

from fastapi import UploadFile
from reportlab.lib.pagesizes import LETTER
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

from job_agent.memory.store import JobStore
from job_agent.generate.resume import parse_resume_pdf
from job_agent.generate.cover_letter import generate_cover_letter_gpt


store = JobStore("job_agent/data/jobs.db")

OUTPUT_DIR = "generated_letters"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def generate_cover_letter(
    resume_file: UploadFile,
    job_ids: List[str],
):
    """
    Generate cover letters for selected job_ids using uploaded resume.
    """

    results = []

    # --------------------------------------------------
    # 1. Save uploaded resume to temp file
    # --------------------------------------------------
    with NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(resume_file.file.read())
        resume_path = tmp.name

    # --------------------------------------------------
    # 2. Parse resume ONCE
    # --------------------------------------------------
    resume_text = parse_resume_pdf(resume_path)

    # --------------------------------------------------
    # 3. Generate cover letter per job
    # --------------------------------------------------
    for job_id in job_ids:
        job = store.load_job(job_id)
        job_text = store.load_job_detail(job_id)

        if not job or not job_text:
            continue

        text = generate_cover_letter_gpt(
            resume_text=resume_text,
            job_text=job_text,
            company=job.company,
            role=job.title,
        )

        filename = f"cover_letter_{job_id}.pdf"
        filepath = os.path.join(OUTPUT_DIR, filename)

        doc = SimpleDocTemplate(
            filepath,
            pagesize=LETTER,
            rightMargin=40,
            leftMargin=40,
            topMargin=40,
            bottomMargin=40,
        )

        styles = getSampleStyleSheet()
        style = styles["Normal"]

        story = []
        for para in text.split("\n\n"):
            story.append(Paragraph(para.replace("\n", "<br/>"), style))

        doc.build(story)

        results.append({"filename": filename})

    # --------------------------------------------------
    # 4. Cleanup temp resume
    # --------------------------------------------------
    os.remove(resume_path)

    return results
