import asyncio 
import csv

from app.db.session import AsyncSessionLocal
from app.services.source_registry_service import SourceRegistryService


async def main() -> None:
    imported = 0

    async with AsyncSessionLocal() as session:
        registry = SourceRegistryService(session)

        with open("data/company_sources.csv", newline="") as file:
            reader = csv.DictReader(file)

            for row in reader: 
                await registry.register_source(
                    provider=row["provider"],
                    identifier=row["identifier"],
                    display_name=row["display_name"],
                )
                imported += 1

        await session.commit()

    print(f"Imported {imported} sources.")

if __name__ == "__main__":
    asyncio.run(main())