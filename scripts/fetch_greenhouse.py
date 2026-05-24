import asyncio

from app.sources.greenhouse import GreenhouseSource

async def main() -> None:
    source = GreenhouseSource(
        board_token="airbnb",
        company_name="Airbnb",
    )

    jobs = await source.fetch_jobs()

    print(f"Fetched {len(jobs)} jobs")

    for job in jobs[:10]:
        print()
        print(job.title)
        print(job.company)
        print(job.location)
        print(job.absolute_url)


if __name__ == "__main__":
    asyncio.run(main())