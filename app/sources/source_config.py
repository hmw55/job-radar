from dataclasses import dataclass


@dataclass(frozen=True)
class SourceConfig:
    provider: str
    identifier: str
    display_name: str