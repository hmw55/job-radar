from datetime import datetime
from typing import Any

import httpx

from app.sources.base import NormalizedJob


class AshbySource: 
    def __init__(self, organization_slug: str, company_name: str) -> None:
        self.organization_slug = organization_slug
        self.company_name = company_name

    async def fetch_jobs(self) -> list[NormalizedJob]:
        url = f"https://api.ashbyhq.com/posting-api/job-board/{self.organization_slug}"

        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.get(url)
            response.raise_for_status()

        data = response.json()
        jobs = data.get("jobs", [])

        return [self._normalize_job(job) for job in jobs]

    def _normalize_job(self, job: dict[str, Any]) -> NormalizedJob:
        location = job.get("location")
        if isinstance(location, dict):
            location = location.get("name")

        department = job.get("department")
        if isinstance(department, dict):
            department = department.get("name")

        updated_at = None
        if job.get("updatedAt"):
            updated_at = datetime.fromisoformat(job["updatedAt"].replace("Z", "+00:00"))

        description = job.get("descriptionPlain") or job.get("descriptionHtml")

        return NormalizedJob(
            source=f"ashby:{self.organization_slug}",
            source_job_id=str(job["id"]),
            company=self.company_name,
            title=job["title"],
            location=location if isinstance(location, str) else None,
            department=department if isinstance(department, str) else None,
            absolute_url=job["jobUrl"],
            content=description if isinstance(description, str) else None,
            updated_at=updated_at,
        )
        