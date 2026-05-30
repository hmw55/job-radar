import asyncio

from app.db.session import AsyncSessionLocal
from app.repositories.company_source_repository import companySourceRepository
from app.sources.config import ASHBY_SOURCES, GREENHOUSE_SOURCES, LEVER_SOURCES



async def main() -> None:
    sources = [
        *GREENHOUSE_SOURCES,
        *LEVER_SOURCES,
        *ASHBY_SOURCES,
    ]

    async with AsyncSessionLocal() as session:
        repository = companySourceRepository(session)

        for source in sources: 
            await repository.upsert_source(source)

        await session.commit()

    print(f"Seeded {len(sources)} company sources.")


if __name__ == "__main__":
    asyncio.run(main())