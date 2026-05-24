from dataclasses import dataclass, field


@dataclass(frozen=True)
class SearchProfile:
    name: str
    job_titles: list[str]
    keywords: list[str]
    locations: list[str] = field(default_factory=list)
    excluded_titles: list[str] = field(default_factory=list)
    excluded_companies: list[str] = field(default_factory=list)
    experience_levels: list[str] = field(default_factory=list)
    remote_only: bool = False