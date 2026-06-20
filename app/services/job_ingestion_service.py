# ============================================================
# Job Ingestion Service
# ============================================================
#
# This service is responsible for synchronizing jobs from an
# ATS source into the Job Radar database.
#
# During ingestion:
#
# 1. Jobs are fetched from an ATS provider
# 2. Existing jobs are identified
# 3. New jobs are inserted
# 4. Removed jobs are marked inactive
#
# This service acts as the bridge between external ATS
# systems and Job Radar's internal database.
#
# The matching engine does not communicate directly with ATS
# providers. All job data must first pass through ingestion.
# ============================================================

from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.job_repository import JobRepository
from app.sources.base import JobSource


@dataclass(frozen=True)
class IngestionResult:
    # Summary of a single ingestion run.
    # 
    # Attributes: 
    #   fetched_count: 
    #       Total jobs returned by the ATS source.
    # 
    #   new_count: 
    #       New jobs inserted into the database.
    # 
    #   existing_count: 
    #       Jobs already known to Job Radar.
    # 
    #   removed_count: 
    #       Previously active jobs that no longer 
    #       exist in the ATS source. 
    fetched_count: int
    new_count: int
    existing_count: int
    removed_count: int


class JobIngestionService:
    def __init__(self, session: AsyncSession) -> None:
        self.job_repository = JobRepository(session)
        self.session = session

    async def ingest_from_source(self, source: JobSource) -> IngestionResult:
        # Synchronize jobs from an ATS source.
        # 
        # Workflow: 
        # 1. Fetch jobs from the source.
        # 2. Direct removed jobs
        # 3. Insert new jobs
        # 4. Skip existing jobs
        # 5. Commit database changes
        # 
        # Returns:
        #   IngestionResult 

        # Fetch normalized jobs from the ATS provider. 
        # 
        # Each provider is responsible for converting its API
        # response into Job Radar's common job format. 
        jobs = await source.fetch_jobs()

        # Determine which source produces the jobs.
        # 
        # This is later used when identifying jobs that 
        # have been removed from the provider. 
        source_name = jobs[0].source if jobs else "unknown"
        fetched_source_ids = {job.source_job_id for job in jobs}

        active_jobs = await self.job_repository.list_active_jobs_by_source(
            source=source_name,
        )

        removed_count = 0

        # Detect jobs that have disappeared from the ATS. 
        # 
        # If a previously active job is no longer returned by 
        # the provider, it is marked as removed.
        # 
        # This help keeps the registry schronized with the 
        # real-world job board.  
        for active_job in active_jobs:
            if active_job.source_job_id not in fetched_source_ids:
                await self.job_repository.mark_removed(active_job)
                removed_count += 1

        new_count = 0
        existing_count = 0

        for job in jobs:
            # Prevent duplicate job records. 
            # 
            # Jobs are uniquely identified by their ATS source and 
            # source-specific job identifier. 
            exists = await self.job_repository.exists_by_source_id(
                source=job.source,
                source_job_id=job.source_job_id,
            )

            if exists:
                existing_count += 1
                continue

            # Persist newly discovered opportunities.
            # 
            # Only jobs that have not been seen previously are 
            # inserted into the database. 
            await self.job_repository.create_from_normalized_job(job)
            new_count += 1

        # Persist all ingestion changes.
        # 
        # This includes: 
        # - New jobs
        # - Removed jobs
        # 
        # Changes are commited once per ingestion run. 
        await self.session.commit()

        return IngestionResult(
            fetched_count=len(jobs),
            new_count=new_count,
            existing_count=existing_count,
            removed_count=removed_count,
        )