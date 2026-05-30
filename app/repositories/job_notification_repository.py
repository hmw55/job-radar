from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.job_notification import JobNotification


class JobNotificationRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def was_sent(
        self, 
        job_id: int,
        profile_name: str,
        channel: str,
    ) -> bool:
        statement = select(JobNotification.id).where(
            JobNotification.job_id == job_id,
            JobNotification.profile_name == profile_name,
            JobNotification.channel == channel,
        )

        result = await self.session.execute(statement)
        return result.scalar_one_or_none() is not None
    
    async def mark_sent(
        self, 
        job_id: int,
        profile_name: str,
        channel: str,
    ) -> JobNotification:
        notification = JobNotification(
            job_id=job_id,
            profile_name=profile_name,
            channel=channel,
        )

        self.session.add(notification)
        await self.session.flush()

        return notification