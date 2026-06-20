# ============================================================
# Source Discovery Service
# ============================================================
#
# This service automatically discovers ATS job boards used by
# companies.
#
# Given a company name and slug, Job Radar attempts to locate
# supported hiring platforms and automatically register them
# for future ingestion.
#
# Example:
#
#     Company: Vercel
#     Slug: vercel
#
# Job Radar will attempt:
#
#     Greenhouse
#     Lever
#     Ashby
#
# If a valid board is found, the source is automatically
# registered and becomes part of future Job Radar runs.
#
# This allows the registry to grow without manually adding
# every company source.
#
# Note: 
# Source discovery is intentionally conservative
# 
# A company is only registed if Job Radar can verify that 
# a supported ATS provided returns active jobs.
# 
# This helps prevent invalid sources from polluting the 
# registry. 
# ============================================================
from dataclasses import dataclass

import httpx
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.source_registry_service import SourceRegistryService


@dataclass(frozen=True)
class SourceDiscoveryResult:
    # Result returned by a source discovery attempt. 
    # 
    # Attributes: 
    # 
    #   providers: 
    #       ATS provider that was discovered.
    # 
    #   identifiers: 
    #       Provide-specific board identifier.
    # 
    #   display_name:
    #       Human-readable company name.
    # 
    #   discovered: 
    #       Indicated whether a supported ATS board 
    #       was successfully located. 
    provider: str
    identifier: str
    display_name: str
    discovered: bool


class SourceDiscoveryService:
    def __init__(self, session: AsyncSession) -> None:
        self.registry = SourceRegistryService(session)

    # Attempt to discover a supported board for a comapny.
    # 
    # Discovery is performed by testing multiple ATS providers 
    # against several possible slug variations. 
    # 
    # Example: 
    #   Input: 
    #       company_name="DigitalOcean"
    #       slug="digiticalocean"
    # 
    #   Attempts:
    #       greenhouse/digitalocean
    #       level/digitalocean
    #       ashby/digitalocean
    # 
    # The first successful provider is automatically 
    # registered in the source registry.
    # 
    # Returns: 
    #   SourceDiscoveryResult 
    async def discover_source(
        self,
        company_name: str,
        slug: str,
    ) -> SourceDiscoveryResult:
        
        # Generate multiple possible ATS slug variations. 
        #
        # Many companies use slightly different identifiers 
        # than their public company name.
        # 
        # Example: 
        #   Digital Ocean
        #   digitalocean
        #   digital-ocean
        # 
        # Trying multiple variants improves discovery success. 
        slug_variants = self._build_slug_variants(slug)

        # ATS providers currently supported by Job Radar.
        # 
        # New providers can be added here as support is implemented. 
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

    # Generate common ATS slug variations. 
    # 
    # Many ATS boards use naming conventions such as: 
    #   company 
    #   comapny-inc
    #   companyhq
    # 
    # Generating variants increase the likelihood of 
    # successful discovery.  
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

    # Check whether a Greenhouse board exists. 
    #
    # A valid  board must:
    # - Return HTTP 200
    # - Contain at least one active job 
    async def _has_greenhouse_board(self, slug: str) -> bool:
        url = f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs"
        return await self._url_returns_jobs(url)

    # Check whether a Lever board exists. 
    #
    # A valid  board must:
    # - Return HTTP 200
    # - Contain at least one active job 
    async def _has_lever_board(self, slug: str) -> bool:
        url = f"https://api.lever.co/v0/postings/{slug}"
        return await self._url_returns_jobs(url, params={"mode": "json"})

    # Check whether an Ashby board exists. 
    #
    # A valid  board must:
    # - Return HTTP 200
    # - Contain at least one active job 
    async def _has_ashby_board(self, slug: str) -> bool:
        url = f"https://api.ashbyhq.com/posting-api/job-board/{slug}"
        return await self._url_returns_jobs(url)

    # Validate that a potential ATS endpoint contains jobs. 
    # 
    # Requirements:
    # - Successful HTTP response
    # - Valid JSON payload
    # - At least one active job posting
    # 
    # Returns: 
    #   True if the endpoint appears to be a valid ATS board. 
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

            # Different ATS providers return different JSON
            # structures.
            #
            # Some return:
            #
            #     [...]
            #
            # Others return:
            #
            #     {
            #         "jobs": [...]
            #     }
            #
            # Handle both formats.
            if isinstance(data, dict):
                jobs = data.get("jobs")
                return isinstance(jobs, list) and len(jobs) > 0

            return False

        except (httpx.HTTPError, ValueError):
            return False