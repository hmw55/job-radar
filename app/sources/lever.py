from datetime import datetime
from typing import Any

import httpx

from app.sources.base import NormalizedJob

class LeverSource:
    def __init__(self, company_slug: str, company_name: str) -> None:
        self.company_slug = company_slug
        self.company_name = company_name

    async def fetch_jobs(self) -> list[NormalizedJob]:
        url = f"https://api.lever.co/v0/postings/{self.company_slug}"

        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.get(url, params={"mode": "json"})
            response.raise_for_status()

        jobs = response.json()

        return [self._normalize_job(job) for job in jobs]

    def _normalize_job(self, job: dict[str, Any]) -> NormalizedJob:
        categories = job.get("categories") or {}

        location = categories.get("location")
        department = categories.get("department")

        created_at = None
        if job.get("createdAt"):
            created_at = datetime.fromtimestamp(job["createdAt"] / 1000) 

        content_parts = [
            job.get("descriptionPlain"),
            job.get("additionalPlain"),
        ]


        content = "\n\n".join(
            part for part in content_parts if isinstance(part, str) and part.strip()
        )

        return NormalizedJob(
            source=f"lever:{self.company_slug}",
            source_job_id=str(job["id"]),
            company=self.company_name,
            title=job["text"],
            location=location,
            department=department,
            absolute_url=job["hostedUrl"],
            content=content or None,
            updated_at=created_at,
        )