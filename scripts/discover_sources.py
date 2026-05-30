import asyncio
import csv

from app.db.session import AsyncSessionLocal
from app.services.source_discovery_service import SourceDiscoveryService



async def main() -> None:
    discovered_count = 0
    missed_count = 0

    async with AsyncSessionLocal() as session:
        discovery = SourceDiscoveryService(session)

        with open("data/source_candidates.csv", newline="") as file:
            reader = csv.DictReader(file)

            for row in reader: 
                result = await discovery.discover_source(
                    company_name=row["company_name"],
                    slug=row["slug"],
                )

                if result.discovered:
                    discovered_count += 1
                    print (
                        f"Disovered {result.display_name}: "
                        f"{result.provider}:{result.identifier}"
                    )
                else:
                    missed_count += 1
                    print(f"Missed {result.display_name}")

        await session.commit()

if __name__ == "__main__":
    asyncio.run(main())