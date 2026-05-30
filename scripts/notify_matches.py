import asyncio 

from app.core.config import settings
from app.db.session import AsyncSessionLocal
from app.profiles import mack_profile
from app.repositories.job_repository import JobRepository
from app.services.job_matching_service import JobMatchingService
from app.notifications.discord import DiscordNotifier


async def main() -> None:
    if not settings.discord_webhook_url:
        raise RuntimeError("DISCORD_WEBHOOK_URL is not configured.")

    async with AsyncSessionLocal() as session:
        repository = JobRepository(session)
        jobs = await repository.list_jobs(limit=250)

    matcher = JobMatchingService()
    results =  [matcher.match_job(job, mack_profile) for job in jobs]

    matches = [result for result in results if result.matched]
    matches.sort(key=lambda result: result.score, reverse=True)

    notifier = DiscordNotifier(settings.discord_webhook_url)

    for result in matches[:5]:
        await notifier.send_job_match(result)

    print(f"Sent {min(len(matches), 5)} Discord notifications.")

if __name__ == "__main__":
    asyncio.run(main())