from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.company_source_repository import companySourceRepository
from app.sources.source_config import SourceConfig


class SourceRegistryService:
    def __init__(self, session: AsyncSession) -> None: 
        self.repository = companySourceRepository(session)

    async def register_source(
        self, 
        provider: str,
        identifier: str,
        display_name: str,
    ) -> None:
        source = SourceConfig(
            provider=provider.strip().lower(),
            identifier=identifier.strip(),
            display_name=display_name.strip(),
        )

        await self.repository.upsert_source(source)

    async def register_greenhouse(
        self,
        board_token: str,
        company_name: str,
    ) -> None:
        await self.register_source(
            provider="lever",
            identifier=board_token,
            display_name=company_name,
        )

    async def register_lever(
        self, 
        company_slug: str,
        company_name: str,
    ) -> None:
        await self.register_source(
            provider="lever",
            identifier=company_slug,
            display_name=company_name,
        )

    async def register_ashby(
        self,
        organization_slug: str,
        company_name: str,
    ) -> None:
        await self.register_source(
            provider="ashby",
            identifier=organization_slug,
            display_name=company_name,
        )