import json 
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.job_match import JobMatch
from app.services.job_matching_service import JobMatchResult


class JobMatchRepository: 
    def __init__(self, session: AsyncSession) -> None: 
        self.session = session

    async def upsert_match(
            self, 
            result: JobMatchResult,
            profile_name: str,
    ) -> JobMatch:
        statement = select(JobMatch).where(
            JobMatch.job_id == result.job.id,
            JobMatch.profile_name == profile_name,
        )

        existing = (await self.session.execute(statement)).scalar_one_or_none()

        reasons_json = json.dumps(result.reasons)

        if existing: 
            existing.score = result.score
            existing.match_level = result.match_level
            existing.reasons = reasons_json
            existing.matched_at = datetime.utcnow()


            await self.session.flush()
            return existing
        
        job_match = JobMatch(
            job_id=result.job.id,
            profile_name=profile_name,
            score=result.score,
            match_level=result.match_level,
            reasons=reasons_json,
        )

        self.session.add(job_match)
        await self.session.flush()

        return job_match