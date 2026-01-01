# generate/cover_letter.py
from typing import Any


def build_cover_letter_prompt(
    resume_text: str,
    job_text: str,
    company: str,
    role: str,
):
    return [
        {
            "role": "system",
            "content": (
                "You are a senior technical hiring manager and recruiter. "
                "You write professional, concrete, non-generic cover letters."
            ),
        },
        {
            "role": "user",
            "content": f"""
CANDIDATE RESUME
{resume_text}

JOB DESCRIPTION
{job_text}

INSTRUCTIONS
- Write a cover letter for the role: {role} at {company}
- Use ONLY information present in the resume
- Do NOT invent experience or skills
- Be specific and concrete, not generic
- Align candidate experience with job responsibilities
- Keep the tone professional and confident
- Avoid buzzwords and fluff
- Length: 3–4 short paragraphs (max ~350 words)
""".strip(),
        },
    ]


def generate_cover_letter(
    resume_text: str,
    job_text: str,
    company: str,
    role: str,
    llm: Any,
) -> str:
    prompt = build_cover_letter_prompt(
        resume_text=resume_text,
        job_text=job_text,
        company=company,
        role=role,
    )

    return llm.generate(prompt)
