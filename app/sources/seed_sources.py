from app.sources.source_config import SourceConfig


SEED_SOURCES = [
    # Greenhouse
    SourceConfig(provider="greenhouse", identifier="airbnb", display_name="Airbnb"),
    SourceConfig(provider="greenhouse", identifier="stripe", display_name="Stripe"),
    SourceConfig(provider="greenhouse", identifier="vercel", display_name="Vercel"),
    SourceConfig(provider="greenhouse", identifier="datadog", display_name="Datadog"),
    SourceConfig(provider="greenhouse", identifier="digitalocean98", display_name="Digital Ocean"),
    SourceConfig(provider="greenhouse", identifier="elastic", display_name="Elastic"),

    # Ashby    
    SourceConfig(provider="ashby", identifier="ashby", display_name="Ashby"),
    SourceConfig(provider="ashby", identifier="supabase", display_name="Supabase"),
    SourceConfig(provider="ashby", identifier="render", display_name="Render"),
    SourceConfig(provider="ashby", identifier="posthog", display_name="PostHog"),
    SourceConfig(provider="ashby", identifier="cursor", display_name="Cursor"),
    SourceConfig(provider="ashby", identifier="linear", display_name="Linear"),
    SourceConfig(provider="ashby", identifier="railway", display_name="Railway"),
    SourceConfig(provider="ashby", identifier="retool", display_name="Retool"),

    # Lever
    SourceConfig(provider="lever", identifier="swissborg", display_name="SwissBorg"),
    SourceConfig(provider="lever", identifier="docker", display_name="Docker"),
    SourceConfig(provider="lever", identifier="sourcegraph", display_name="Sourcegraph"),

]