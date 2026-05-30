import asyncio

from app.db.session import AsyncSessionLocal
from app.services.source_discovery_service import SourceDiscoveryService


async def main() -> None:
    company_name = "Vercel"
    slug = "vercel"

    async with AsyncSessionLocal() as session:
        discovery = SourceDiscoveryService(session)

        result = await discovery.discover_source(
            company_name=company_name,
            slug=slug,
        )

        await session.commit()

    if result.discovered: 
        print(
            f"Discovered {result.display_name}: "
            f"{result.provider}:{result.identifier}"
        )
    else:
        print(f"No source discovered for {result.display_name}.")


if __name__ == "__main__":
    asyncio.run(main())