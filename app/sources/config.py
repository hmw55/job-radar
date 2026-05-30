from app.sources.greenhouse import GreenhouseSource
from app.sources.lever import LeverSource
from app.sources.source_config import SourceConfig


GREENHOUSE_SOURCES = [
    SourceConfig(provider="greenhouse", identifier="airbnb", display_name="Airbnb"),
    SourceConfig(provider="greenhouse", identifier="stripe", display_name="Stripe"),
]

LEVER_SOURCES = [
    SourceConfig(provider="lever", identifier="swissborg", display_name="SwissBorg"),
]


def build_greenhouse_sources() -> list[GreenhouseSource]:
    return [
        GreenhouseSource(
            board_token=source.identifier,
            company_name=source.display_name,
        )
        for source in GREENHOUSE_SOURCES
    ]


def build_lever_sources() -> list[LeverSource]:
    return [
        LeverSource(
            company_slug=source.identifier,
            company_name=source.display_name,
        )
        for source in LEVER_SOURCES
    ]


def build_sources() -> list[GreenhouseSource | LeverSource]:
    return [
        *build_greenhouse_sources(),
        *build_lever_sources(),
    ]