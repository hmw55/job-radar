# ============================================================
# Job Radar Service
# ============================================================
#
# This service coordinates the entire Job Radar workflow.
#
# A typical run performs the following steps:
#
# 1. Fetch jobs from an ATS source
# 2. Store new jobs in the database
# 3. Load jobs for evaluation
# 4. Score jobs against a search profile
# 5. Persist match results
# 6. Send Discord notifications
# 7. Record notification history
#
# This is effectively the main orchestration layer of the
# application.
#
# Most high-level Job Radar behavior eventually flows through
# this service.
# ============================================================
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from app.notifications.discord import DiscordNotifier
from app.profiles.search_profile import SearchProfile
from app.repositories.job_match_repository import JobMatchRepository
from app.repositories.job_notification_repository import JobNotificationRepository
from app.repositories.job_repository import JobRepository
from app.services.job_ingestion_service import JobIngestionService
from app.services.job_matching_service import JobMatchingService
from app.sources.base import JobSource


@dataclass(frozen=True)
class JobRadarRunResult:
    # Summary of a single Job Radar execution.
    # 
    # These values are used for logging, debugging, monitoring, 
    # and future analytics.
    # 
    # Example: 
    #   Source: Airbnb
    #   Fetched: 150
    #   New: 12
    #   Matches: 4
    #   Sent: 4 
    fetched_count: int
    new_count: int
    existing_count: int
    removed_count: int
    matched_count: int
    sent_count: int
    skipped_count: int
    failed_count: int
    failure_reasons: list[str]


class JobRadarService:
    def __init__(
        self,
        session: AsyncSession,
        notifier: DiscordNotifier,
    ) -> None:
        self.session = session
        self.notifier = notifier
        self.ingestion_service = JobIngestionService(session)
        self.job_repository = JobRepository(session)
        self.notification_repository = JobNotificationRepository(session)
        self.matching_service = JobMatchingService()
        self.match_repository = JobMatchRepository(session)

    # Execute a complete Job Radar run against a single ATS source.
    # 
    # Workflow: 
    # 1. Ingest jobs from the source
    # 2. Load stored jobs
    # 3. Evaluate jobs against the search profile
    # 4. Save match results
    # 5. Send Discord notifications
    # 6. Record notification history
    # 7. Commit database changes
    # 
    # Returns: 
    #   JobRadarRunResult 
    async def run_once(
        self,
        source: JobSource,
        profile: SearchProfile,
        notification_limit: int = 5,
    ) -> JobRadarRunResult:
        ingestion_result = await self.ingestion_service.ingest_from_source(source)

        # Evaluate a subset of the most recently stored jobs. 
        # 
        # This limit prevents large registries from causing 
        # excessively long matching runs. 
        # 
        # Future version may make this configurable. 
        jobs = await self.job_repository.list_jobs(limit=250)
        results = [self.matching_service.match_job(job, profile) for job in jobs]

        matches = [result for result in results if result.matched]

        # Highest-scoring opportunities are prioritized first. 
        # 
        # This ensures notification limits favor the strongest 
        # opportunities available. 
        matches.sort(key=lambda result: result.score, reverse=True)

        for result in matches:
            await self.match_repository.upsert_match(
                result=result,
                profile_name=profile.name,
            )

        sent_count = 0
        skipped_count = 0

        for result in matches:
            if notification_limit == 0:
                break

            # Notification Throttling. 
            # 
            # Limits the number of notifications sent during 
            # a single run to avoid overwhelming users and 
            # Discord channels. 
            if notification_limit > 0 and sent_count >= notification_limit:
                break

            job = result.job


            # Prevent duplicate Discord notification. 
            # 
            # A job may remain in the database for multiple runs. 
            # This check ensures users receive each matching job 
            # only once per profile/channel combination. 
            already_sent = await self.notification_repository.was_sent(
                job_id=job.id,
                profile_name=profile.name,
                channel="discord",
            )

            if already_sent:
                skipped_count += 1
                continue

            await self.notifier.send_job_match(result)

            await self.notification_repository.mark_sent(
                job_id=job.id,
                profile_name=profile.name,
                channel="discord",
            )

            sent_count += 1

        # Persis: 
        # - Job changes
        # - Match records
        # - Norification history
        # 
        # Everything is committed at the end of the run 
        # to keep execution atomic. 
        await self.session.commit()

        return JobRadarRunResult(
            fetched_count=ingestion_result.fetched_count,
            new_count=ingestion_result.new_count,
            existing_count=ingestion_result.existing_count,
            removed_count=ingestion_result.removed_count,
            matched_count=len(matches),
            sent_count=sent_count,
            skipped_count=skipped_count,
            failed_count=0,
            failure_reasons=[],
        )
    