import asyncio

from app.core.config import settings
from app.db.session import AsyncSessionLocal
from app.notifications.discord import DiscordNotifier
from app.profiles import mack_profile
from app.services.job_radar_service import JobRadarService
from app.sources.config import build_greenhouse_sources


async def main() -> None:
    if not settings.discord_webhook_url:
        raise RuntimeError("DISCORD_WEBHOOK_URL is not configured.")

    notifier = DiscordNotifier(settings.discord_webhook_url)

    total_fetched = 0
    total_new = 0
    total_existing = 0
    total_removed = 0
    total_matches = 0
    total_sent = 0
    total_skipped = 0

    async with AsyncSessionLocal() as session:
        service = JobRadarService(
            session=session,
            notifier=notifier,
        )

        for source in build_greenhouse_sources():
            result = await service.run_once(
                source=source,
                profile=mack_profile,
                notification_limit=settings.notification_limit,
            )

            total_fetched += result.fetched_count
            total_new += result.new_count
            total_existing += result.existing_count
            total_removed += result.removed_count
            total_matches += result.matched_count
            total_sent += result.sent_count
            total_skipped += result.skipped_count

    print(f"Fetched: {total_fetched}")
    print(f"New: {total_new}")
    print(f"Existing: {total_existing}")
    print(f"Removed: {total_removed}")
    print(f"Matches: {total_matches}")
    print(f"Sent: {total_sent}")
    print(f"Skipped: {total_skipped}")


if __name__ == "__main__":
    asyncio.run(main())