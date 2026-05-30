import asyncio
from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler  # type: ignore[import-untyped]

from app.core.config import settings
from scripts.run_job_radar import main as run_job_radar


async def scheduled_run() -> None:
    print()
    print(f"[{datetime.now().isoformat(timespec='seconds')}] Running Job Radar...")

    try:
        await run_job_radar()
        print(f"Waiting {settings.poll_interval_minutes} minutes...")
    except Exception as error:
        print(f"Job Radar run failed: {error}")


async def main() -> None:
    scheduler = AsyncIOScheduler()

    scheduler.add_job(
        scheduled_run,
        trigger="interval",
        minutes=settings.poll_interval_minutes,
        id="job_radar_poll",
        replace_existing=True,
    )

    scheduler.start()

    print("Job Radar scheduler started.")
    print(f"Polling every {settings.poll_interval_minutes} minutes.")
    print("Press Ctrl+C to stop.")

    await scheduled_run()

    try:
        while True:
            await asyncio.sleep(1)
    finally:
        scheduler.shutdown()
        print("Scheduler stopped.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass