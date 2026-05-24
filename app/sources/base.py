from dataclasses import dataclass 
from datetime import datetime
from typing import Protocol

@dataclass(frozen=True)
class NormalizedJob:
    source: str
    source_job_id: str
    company: str
    title: str
    location: str | None
    department: str | None
    absolute_url: str 
    content: str | None
    updated_at: datetime | None


class JobSource(Protocol):
    async def fetch_jobs(self) -> list[NormalizedJob]:
        """Fetch and normalize jobs from a public job source."""