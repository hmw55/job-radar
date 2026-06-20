import asyncio

from app.core.config import settings
from app.db.session import AsyncSessionLocal
from app.notifications.discord import DiscordNotifier
from app.profiles import default_profile
from app.services.job_radar_service import JobRadarService
from app.repositories.company_source_repository import companySourceRepository
from app.sources.factory import build_source_from_company_source


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
    total_failed = 0
    failure_reasons: list[str] = []

    async with AsyncSessionLocal() as session:
        service = JobRadarService(
            session=session,
            notifier=notifier,
        )

        company_source_repository = companySourceRepository(session)
        company_sources = await company_source_repository.list_active_sources()

        for company_source in company_sources:
            source = build_source_from_company_source(company_source)
            try:
                result = await service.run_once(
                    source=source,
                    profile=default_profile,
                    notification_limit=settings.notification_limit,
                )
            except Exception as error:
                total_failed += 1
                failure_reasons.append(str(error))
                continue

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
    
    print(f"Failed Sources: {total_failed}")

    if failure_reasons:
        print("Failure Reasons:")
        for reason in failure_reasons: 
            print(f"- {reason}")

    print(f"Sources Polled: {len(company_sources)}")

if __name__ == "__main__":
    asyncio.run(main())