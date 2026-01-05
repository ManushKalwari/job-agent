from typing import List
from job_agent.memory.store import JobStore
from job_agent.generate.cover_letter import generate_cover_letter_gpt
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
import os
from fastapi import UploadFile

store = JobStore("job_agent/data/jobs.db")

OUTPUT_DIR = "generated_letters"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def generate_cover_letter(resume_file: UploadFile, job_ids: list[str],):
    results = []

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

        c = canvas.Canvas(filepath, pagesize=LETTER)
        width, height = LETTER

        y = height - 40
        for line in text.split("\n"):
            c.drawString(40, y, line)
            y -= 14
            if y < 40:
                c.showPage()
                y = height - 40

        c.save()

        results.append({"filename": filename})

    return results