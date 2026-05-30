from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.company_source import CompanySource
from app.sources.source_config import SourceConfig


class companySourceRepository: 
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list_active_sources(self) -> list[CompanySource]:
        statement = (
            select(CompanySource)
            .where(CompanySource.is_active.is_(True))
            .order_by(CompanySource.provider, CompanySource.display_name)
        )

        result = await self.session.execute(statement)
        return list(result.scalars().all())

    async def upsert_source(self, source: SourceConfig) -> CompanySource:
        statement = select(CompanySource).where(
            CompanySource.provider == source.provider,
            CompanySource.identifier == source.identifier,
        )

        existing = (await self.session.execute(statement)).scalar_one_or_none()

        if existing: 
            existing.display_name = source.display_name
            existing.is_active = True
            await self.session.flush()
            return existing
        
        company_source = CompanySource(
            provider=source.provider,
            identifier=source.identifier,
            display_name=source.display_name,
            is_active=True,
        )

        self.session.add(company_source)
        await self.session.flush()

        return company_source