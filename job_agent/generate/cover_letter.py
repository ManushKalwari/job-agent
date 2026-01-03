# generate/cover_letter.py
from typing import Any
from openai import OpenAI
import os


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
<<CANDIDATE RESUME>>
{resume_text}

<<JOB DESCRIPTION>>
{job_text}

<<INSTRUCTIONS>>
- Write a cover letter for the role: {role} at {company}
- Use ONLY information present in the resume. Do NOT invent experience or skills.
- Align candidate experience with job responsibilities
- Keep the tone professional and confident. Avoid buzzwords and fluff
- Length: 3–4 short paragraphs (max ~350 words)
""".strip(),
        },
    ]




def generate_cover_letter_local(
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




def generate_cover_letter_gpt(
    resume_text: str,
    job_text: str,
    company: str,
    role: str,
) -> str:
    
    client = OpenAI() 

    messages = build_cover_letter_prompt(
        resume_text=resume_text,
        job_text=job_text,
        company=company,
        role=role,
    )

    prompt = "\n\n".join(
        f"{m['role'].upper()}:\n{m['content']}" for m in messages
    )

    resp = client.responses.create(
        model="gpt-5-nano",
        input=prompt,
    )

    if not resp.output_text:
        raise RuntimeError("Empty OpenAI output")

    return resp.output_text
