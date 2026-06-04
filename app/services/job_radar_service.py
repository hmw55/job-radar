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

    async def run_once(
        self,
        source: JobSource,
        profile: SearchProfile,
        notification_limit: int = 5,
    ) -> JobRadarRunResult:
        ingestion_result = await self.ingestion_service.ingest_from_source(source)

        jobs = await self.job_repository.list_jobs(limit=250)
        results = [self.matching_service.match_job(job, profile) for job in jobs]

        matches = [result for result in results if result.matched]
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

            if notification_limit > 0 and sent_count >= notification_limit:
                break

            job = result.job

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
    