import asyncio

from app.db.session import AsyncSessionLocal
from app.services.source_registry_service import SourceRegistryService
from app.sources.seed_sources import SEED_SOURCES


async def main() -> None:
    async with AsyncSessionLocal() as session:
        registry = SourceRegistryService(session)

        for source in SEED_SOURCES:
            await registry.register_source(
                provider=source.provider,
                identifier=source.identifier,
                display_name=source.display_name,
            )

        await session.commit()

    print(f"Seeded {len(SEED_SOURCES)} company sources.")


if __name__ == "__main__":
    asyncio.run(main())