from app.sources.source_config import SourceConfig


SEED_SOURCES = [
    SourceConfig(provider="greenhouse", identifier="airbnb", display_name="Airbnb"),
    SourceConfig(provider="greenhouse", identifier="stripe", display_name="Stripe"),
    SourceConfig(provider="lever", identifier="swissborg", display_name="SwissBord"),
    SourceConfig(provider="ashby", identifier="ashby", display_name="Ashby"),
]