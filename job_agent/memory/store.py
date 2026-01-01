# memory/store.py
import sqlite3
from typing import Iterable, List
from datetime import datetime
from pathlib import Path

from job_agent.models.job import JobPosting


class JobStore:
    def __init__(self, db_path: str):
        base_dir = Path(__file__).resolve().parents[1]  # job_agent/
        self.db_path = base_dir / db_path

        # ensure directory exists
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        self._init_db()

    def _connect(self):
        return sqlite3.connect(self.db_path, check_same_thread=False)

    def _init_db(self):
        with self._connect() as conn:
            # jobs table
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS jobs (
                    job_id TEXT PRIMARY KEY,
                    company TEXT,
                    title TEXT,
                    location TEXT,
                    description TEXT,
                    apply_url TEXT,
                    posted_date TEXT,
                    source TEXT,
                    first_seen_at TEXT
                )
                """
            )

            # enriched job details
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS job_details (
                    job_id TEXT PRIMARY KEY,
                    full_text TEXT,
                    fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

            conn.commit()

    # ----------------------------
    # Job ingestion
    # ----------------------------
    def save_jobs(self, jobs: Iterable[JobPosting]) -> int:
        inserted = 0
        now = datetime.utcnow().isoformat()

        with self._connect() as conn:
            for job in jobs:
                try:
                    conn.execute(
                        """
                        INSERT INTO jobs (
                            job_id, company, title, location,
                            description, apply_url, posted_date,
                            source, first_seen_at
                        )
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            job.job_id,
                            job.company,
                            job.title,
                            job.location,
                            job.description,
                            job.apply_url,
                            job.posted_date.isoformat() if job.posted_date else None,
                            job.source,
                            now,
                        ),
                    )
                    inserted += 1
                except sqlite3.IntegrityError:
                    continue

            conn.commit()

        return inserted

    def load_all_jobs(self) -> List[JobPosting]:
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT job_id, company, title, location,
                       description, apply_url, posted_date, source
                FROM jobs
                """
            ).fetchall()

        jobs = []
        for row in rows:
            posted_date = (
                datetime.fromisoformat(row[6]).date()
                if row[6]
                else None
            )

            jobs.append(
                JobPosting(
                    job_id=row[0],
                    company=row[1],
                    title=row[2],
                    location=row[3],
                    description=row[4],
                    apply_url=row[5],
                    posted_date=posted_date,
                    source=row[7],
                )
            )

        return jobs

    # ----------------------------
    # Job enrichment
    # ----------------------------
    def save_job_detail(self, job_id: str, full_text: str):
        with self._connect() as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO job_details (job_id, full_text)
                VALUES (?, ?)
                """,
                (job_id, full_text),
            )
            conn.commit()

    def load_job_detail(self, job_id: str) -> str | None:
        with self._connect() as conn:
            row = conn.execute(
                """
                SELECT full_text
                FROM job_details
                WHERE job_id = ?
                """,
                (job_id,),
            ).fetchone()

        return row[0] if row else None
