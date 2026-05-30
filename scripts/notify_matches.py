import asyncio 

from app.core.config import settings
from app.db.session import AsyncSessionLocal
from app.profiles import mack_profile
from app.repositories.job_repository import JobRepository
from app.services.job_matching_service import JobMatchingService
from app.notifications.discord import DiscordNotifier
from app.repositories.job_notification_repository import JobNotificationRepository


async def main() -> None:
    if not settings.discord_webhook_url:
        raise RuntimeError("DISCORD_WEBHOOK_URL is not configured.")

    async with AsyncSessionLocal() as session:
        repository = JobRepository(session)
        notification_repository = JobNotificationRepository(session)

        jobs = await repository.list_jobs(limit=250)

        matcher = JobMatchingService()
        results =  [matcher.match_job(job, mack_profile) for job in jobs]

        matches = [result for result in results if result.matched]
        matches.sort(key=lambda result: result.score, reverse=True)

        notifier = DiscordNotifier(settings.discord_webhook_url)

        sent_count = 0
        skipped_count = 0

        for result in matches[:5]:
            job = result.job

            already_sent = await notification_repository.was_sent(
                job_id=job.id,
                profile_name=mack_profile.name,
                channel="discord",
            )

            if already_sent:
                skipped_count += 1
                continue

            await notifier.send_job_match(result)

            await notification_repository.mark_sent(
                job_id=job.id,
                profile_name=mack_profile.name,
                channel="discord",
            )

            sent_count += 1
        
        await session.commit()

    print(f"Sent {sent_count} Discord notifications.")
    print(f"Skipped {skipped_count} already-sent notifications.")

if __name__ == "__main__":
    asyncio.run(main())