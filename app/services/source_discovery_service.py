from dataclasses import dataclass

import httpx
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.source_registry_service import SourceRegistryService


@dataclass(frozen=True)
class SourceDiscoveryResult:
    provider: str
    identifier: str
    display_name: str
    discovered: bool


class SourceDiscoveryService:
    def __init__(self, session: AsyncSession) -> None:
        self.registry = SourceRegistryService(session)

    async def discover_source(
        self,
        company_name: str,
        slug: str,
    ) -> SourceDiscoveryResult:
        slug_variants = self._build_slug_variants(slug)

        discovery_attempts = [
            ("greenhouse", self._has_greenhouse_board),
            ("lever", self._has_lever_board),
            ("ashby", self._has_ashby_board),
        ]

        for candidate_slug in slug_variants:
            for provider, checker in discovery_attempts:
                if await checker(candidate_slug):
                    await self.registry.register_source(
                        provider=provider,
                        identifier=candidate_slug,
                        display_name=company_name.strip(),
                    )

                    return SourceDiscoveryResult(
                        provider=provider,
                        identifier=candidate_slug,
                        display_name=company_name.strip(),
                        discovered=True,
                    )

        return SourceDiscoveryResult(
            provider="unknown",
            identifier=slug_variants[0],
            display_name=company_name.strip(),
            discovered=False,
        )

    def _build_slug_variants(self, slug: str) -> list[str]:
        normalized = slug.strip().lower()
        dashed = normalized.replace(" ", "-")
        compact = normalized.replace("-", "").replace(" ", "")

        variants = [
            normalized,
            dashed,
            compact,
            f"{compact}inc",
            f"{compact}-inc",
            f"{compact}hq",
            f"{compact}-hq",
        ]

        return list(dict.fromkeys(variants))

    async def _has_greenhouse_board(self, slug: str) -> bool:
        url = f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs"
        return await self._url_returns_jobs(url)

    async def _has_lever_board(self, slug: str) -> bool:
        url = f"https://api.lever.co/v0/postings/{slug}"
        return await self._url_returns_jobs(url, params={"mode": "json"})

    async def _has_ashby_board(self, slug: str) -> bool:
        url = f"https://api.ashbyhq.com/posting-api/job-board/{slug}"
        return await self._url_returns_jobs(url)

    async def _url_returns_jobs(
        self,
        url: str,
        params: dict[str, str] | None = None,
    ) -> bool:
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(url, params=params)

            if response.status_code != 200:
                return False

            data = response.json()

            if isinstance(data, list):
                return len(data) > 0

            if isinstance(data, dict):
                jobs = data.get("jobs")
                return isinstance(jobs, list) and len(jobs) > 0

            return False

        except (httpx.HTTPError, ValueError):
            return False