import asyncio

from app.db.session import AsyncSessionLocal
from app.services.job_ingestion_service import JobIngestionService
from app.sources.greenhouse import GreenhouseSource


async def main() -> None:
    source = GreenhouseSource(
        board_token="airbnb",
        company_name="Airbnb",
    )

    async with AsyncSessionLocal() as session:
        service = JobIngestionService(session)
        result = await service.ingest_from_source(source)

    print(f"Fetched: {result.fetched_count}")
    print(f"New: {result.new_count}")
    print(f"Existing: {result.existing_count}")
    print(f"Removed: {result.removed_count}")


if __name__ == "__main__":
    asyncio.run(main())