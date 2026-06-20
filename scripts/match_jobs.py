import asyncio

from app.db.session import AsyncSessionLocal
from app.profiles import default_profile
from app.repositories.job_repository import JobRepository
from app.services.job_matching_service import JobMatchingService


async def main() -> None:
    async with AsyncSessionLocal() as session:
        repository = JobRepository(session)
        jobs = await repository.list_jobs(limit=250)

    matcher = JobMatchingService()
    results = [matcher.match_job(job, default_profile) for job in jobs]

    matches = [result for result in results if result.matched]
    matches.sort(key=lambda result: result.score, reverse=True)

    print(f"Checked: {len(results)}")
    print(f"Matches: {len(matches)}")
    print()

    for result in matches[:25]:
        job = result.job
        print(f"{job.title} — {job.company}")
        print(f"Score:{result.match_level} ({result.score})")
        print(f"Location: {job.location}")
        print(f"URL: {job.absolute_url}")
        print("Reasons:")
        for reason in result.reasons:
            print(f"- {reason}")
        print()


if __name__ == "__main__":
    asyncio.run(main())