from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from app.models.job import Job
from app.sources.base import NormalizedJob


class JobRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def exists_by_source_id(self, source: str, source_job_id: str) -> bool:
        statement = select(Job.id).where(
            Job.source == source, 
            Job.source_job_id == source_job_id,
        )

        result = await self.session.execute(statement)
        return result.scalar_one_or_none() is not None
    
    async def create_from_normalized_job(self, job: NormalizedJob) -> Job:
        db_job = Job(
            source=job.source,
            source_job_id=job.source_job_id,
            company=job.company,
            title=job.title,
            location=job.location,
            department=job.department,
            absolute_url=job.absolute_url,
            content=job.content,
            source_updated_at=job.updated_at,
        )

        self.session.add(db_job)
        await self.session.flush()

        return db_job
    
    async def list_jobs(self, limit: int = 100) -> list[Job]:
        statement = select(Job).order_by(Job.first_seen_at.desc()).limit(limit)

        result = await self.session.execute(statement)
        return list(result.scalars().all())
    
    async def list_active_jobs_by_source(self, source: str) -> list[Job]:
        statement = select(Job).where(
            Job.source == source,
            Job.is_active.is_(True),
        )

        result = await self.session.execute(statement)
        return list(result.scalars().all())

    async def mark_removed(self, job: Job) -> Job:
        job.is_active = False
        job.removed_at = datetime.utcnow()

        await self.session.flush()

        return job