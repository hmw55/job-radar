import asyncio

from app.core.config import settings
from app.db.session import AsyncSessionLocal
from app.notifications.discord import DiscordNotifier
from app.profiles import mack_profile
from app.services.job_radar_service import JobRadarService
from app.sources.greenhouse import GreenhouseSource


async def main() -> None: 
    if not settings.discord_webhook_url:
        raise RuntimeError("DISCORD_WEBHOOK_URL is not configured.")

    source = GreenhouseSource(
        board_token="airbnb",
        company_name="Airbnb",
    )

    notifier = DiscordNotifier(settings.discord_webhook_url)

    async with AsyncSessionLocal() as session: 
        service = JobRadarService(
            session=session,
            notifier=notifier,
        )

        result = await service.run_once(
            source=source, 
            profile=mack_profile,
            notification_limit=settings.notification_limit,
        )

    print(f"Fetched: {result.fetched_count}")
    print(f"New: {result.new_count}")
    print(f"Existing: {result.existing_count}")
    print(f"Matches: {result.matched_count}")
    print(f"Sent: {result.sent_count}")
    print(f"Skipped: {result.skipped_count}")


if __name__ == "__main__":
    asyncio.run(main())