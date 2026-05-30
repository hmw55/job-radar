import asyncio 

from app.db.session import AsyncSessionLocal
from app.services.source_registry_service import SourceRegistryService


async def main() -> None:
    async with AsyncSessionLocal() as session:
        registry = SourceRegistryService(session)

        await registry.register_greenhouse(
            board_token="airbnb",
            company_name="Airbnb",
        )

        await session.commit()

    print("Source registered.")


if __name__ == "__main__":
    asyncio.run(main())