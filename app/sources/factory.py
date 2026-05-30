from app.models.company_source import CompanySource
from app.sources.ashby import AshbySource
from app.sources.base import JobSource
from app.sources.greenhouse import GreenhouseSource
from app.sources.lever import LeverSource


def build_source_from_company_source(company_source: CompanySource) -> JobSource:
    provider = company_source.provider.strip().lower()

    if provider == "greenhouse":
        return GreenhouseSource(
            board_token=company_source.identifier,
            company_name=company_source.display_name,
        )

    if provider == "lever":
        return LeverSource(
            company_slug=company_source.identifier,
            company_name=company_source.display_name,
        )

    if provider == "ashby":
        return AshbySource(
            organization_slug=company_source.identifier,
            company_name=company_source.display_name,
        )

    raise ValueError(f"Unsupported source provider: {company_source.provider}")