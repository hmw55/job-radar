from dataclasses import dataclass

from app.sources.source_config import SourceConfig

from app.sources.greenhouse import GreenhouseSource
from app.sources.lever import LeverSource


@dataclass(frozen=True)
class GreenhouseBoardConfig:
    board_token: str
    company_name: str


GREENHOUSE_BOARDS = [
    GreenhouseBoardConfig(board_token="airbnb", company_name="Airbnb"),
    GreenhouseBoardConfig(board_token="stripe", company_name="Stripe"),
]

LEVER_COMPANIES = [
    SourceConfig(provider="lever", identifier="swissborg", display_name="SwissBorg"),
]

def build_greenhouse_sources() -> list[GreenhouseSource]:
    return [
        GreenhouseSource(
            board_token=board.board_token,
            company_name=board.company_name,
        )
        for board in GREENHOUSE_BOARDS
    ]

def build_lever_sources() -> list[LeverSource]:
    return [
        LeverSource(
            company_slug=company.identifier,
            company_name=company.display_name,
        )
        for company in LEVER_COMPANIES
    ]

def build_sources() -> list [GreenhouseSource | LeverSource]:
    return [
        *build_greenhouse_sources(),
        *build_lever_sources(),
    ]