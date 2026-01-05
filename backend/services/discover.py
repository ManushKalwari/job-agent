# backend/services/discover.py

from job_agent.ingest.greenhouse import fetch_jobs
from job_agent.ingest.parser import parse_greenhouse_job
from job_agent.rank.lexical import LexicalScorer
from job_agent.rank.semantic import SemanticScorer
from job_agent.rank.ranker import poe_score
from job_agent.models.profile import UserProfile
import statistics

def discover_jobs(profile):

    # 1. build profile object
    user_profile = UserProfile(
        target_roles=profile.target_roles,
        core_skills=profile.core_skills,
        location=profile.location,
    )

    query_text = " ".join(user_profile.target_roles + user_profile.core_skills)


    # 2. fetch jobs (for now fixed companies)
    companies = ["airbnb", "stripe", "databricks"]
    jobs = []

    for c in companies:
        raw = fetch_jobs(c)
        jobs.extend(parse_greenhouse_job(j, c) for j in raw)

    job_texts = [f"{j.title or ''} {j.description or ''}" for j in jobs]
    job_ids = [j.job_id for j in jobs]


    # 3. lexical
    lex = LexicalScorer() 
    lex.fit(job_texts, job_ids)
    lex_scores = lex.score_query(query_text)


    # 4. semantic
    sem = SemanticScorer()
    job_embs = sem.embed(job_texts)
    query_emb = sem.embed([query_text])[0]

    
    # 5. scoring
    sem_vals = []
    lex_vals = []

    for job, emb in zip(jobs, job_embs):
        sem_vals.append(sem.similarity(query_emb, emb))
        lex_vals.append(lex_scores.get(job.job_id, 0.0))

    mu_s = statistics.fmean(sem_vals)
    sd_s = statistics.pstdev(sem_vals) or 1e-9
    mu_l = statistics.fmean(lex_vals)
    sd_l = statistics.pstdev(lex_vals) or 1e-9

    # second pass to score
    scored = []
    for job, s_sem, s_lex in zip(jobs, sem_vals, lex_vals):
        poe = poe_score(s_sem, s_lex, mu_s, sd_s, mu_l, sd_l)
        scored.append({"job": job, "poe": poe})

    # 6. sort top 10
    scored.sort(key=lambda x: x["poe"], reverse=True)
    top = scored[:10]

    # 7. response
    return [
        {
            "job_id": r["job"].job_id,
            "title": r["job"].title,
            "company": r["job"].company,
            "location": r["job"].location,
            "apply_url": r["job"].apply_url,
            "poe": r["poe"],
        }
        for r in top
    ]
