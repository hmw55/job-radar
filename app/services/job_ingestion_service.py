from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.job_repository import JobRepository
from app.sources.base import JobSource


@dataclass(frozen=True)
class IngestionResult:
    fetched_count: int
    new_count: int
    existing_count: int
    removed_count: int


class JobIngestionService:
    def __init__(self, session: AsyncSession) -> None:
        self.job_repository = JobRepository(session)
        self.session = session

    async def ingest_from_source(self, source: JobSource) -> IngestionResult:
        jobs = await source.fetch_jobs()

        source_name = jobs[0].source if jobs else "unknown"
        fetched_source_ids = {job.source_job_id for job in jobs}

        active_jobs = await self.job_repository.list_active_jobs_by_source(
            source=source_name,
        )

        removed_count = 0

        for active_job in active_jobs:
            if active_job.source_job_id not in fetched_source_ids:
                await self.job_repository.mark_removed(active_job)
                removed_count += 1

        new_count = 0
        existing_count = 0

        for job in jobs:
            exists = await self.job_repository.exists_by_source_id(
                source=job.source,
                source_job_id=job.source_job_id,
            )

            if exists:
                existing_count += 1
                continue

            await self.job_repository.create_from_normalized_job(job)
            new_count += 1

        await self.session.commit()

        return IngestionResult(
            fetched_count=len(jobs),
            new_count=new_count,
            existing_count=existing_count,
            removed_count=removed_count,
        )