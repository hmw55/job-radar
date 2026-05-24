from datetime import datetime
from typing import Any

import httpx

from app.sources.base import NormalizedJob


class GreenhouseSource:
    def __init__(self, board_token: str, company_name: str) -> None:
        self.board_token = board_token
        self.company_name = company_name

    async def fetch_jobs(self) -> list[NormalizedJob]:
        url = f"https://boards-api.greenhouse.io/v1/boards/{self.board_token}/jobs"

        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.get(url, params={"content": "true"})
            response.raise_for_status()

        data = response.json()
        jobs = data.get("jobs", [])

        return [self._normalize_job(job) for job in jobs]

    def _normalize_job(self, job: dict[str, Any]) -> NormalizedJob:
        offices = job.get("offices") or []
        departments = job.get("departments") or []

        location = None
        if offices:
            location = offices[0].get("name")

        department = None
        if departments:
            department = departments[0].get("name")

        updated_at = None
        if job.get("updated_at"):
            updated_at = datetime.fromisoformat(job["updated_at"].replace("Z", "+00:00"))

        return NormalizedJob(
            source="greenhouse",
            source_job_id=str(job["id"]),
            company=self.company_name,
            title=job["title"],
            location=location,
            department=department,
            absolute_url=job["absolute_url"],
            content=job.get("content"),
            updated_at=updated_at,
        )