from dataclasses import dataclass, field

from app.models.job import Job
from app.profiles.search_profile import SearchProfile

# Match thresholds
MINIMUM_MATCH_SCORE = 50
STRONG_MATCH_SCORE = 70
EXCELLENT_MATCH_SCORE = 90

# Score contributions
TITLE_MATCH_SCORE = 50
KEYWORD_MATCH_SCORE = 10
LOCATION_MATCH_SCORE = 10
EXPERIENCE_MATCH_SCORE = 10
MAX_KEYWORD_SCORE = 40


@dataclass(frozen=True)
class JobMatchResult:
    job: Job
    matched: bool
    score: int
    match_level: str
    reasons: list[str] = field(default_factory=list)


class JobMatchingService:
    def match_job(self, job: Job, profile: SearchProfile) -> JobMatchResult:
        searchable_text = self._build_searchable_text(job)
        title = job.title.lower()
        company = job.company.lower()

        reasons: list[str] = []
        score = 0

        if self._contains_any(title, profile.excluded_titles):
            return JobMatchResult(
                job=job,
                matched=False,
                score=0,
                match_level="NO MATCH",
                reasons=["Excluded title"],
            )

        if self._contains_any(company, profile.excluded_companies):
            return JobMatchResult(
                job=job,
                matched=False,
                score=0,
                match_level="NO MATCH",
                reasons=["Excluded company"],
            )

        matched_titles = self._matched_terms(title, profile.job_titles)
        if matched_titles:
            score += TITLE_MATCH_SCORE
            reasons.append(f"Matched title: {', '.join(matched_titles)}")

        matched_keywords = self._matched_terms(searchable_text, profile.keywords)
        if matched_keywords:
            score += min(
                len(matched_keywords) * KEYWORD_MATCH_SCORE,
                MAX_KEYWORD_SCORE,
            )
            reasons.append(f"Matched keywords: {', '.join(matched_keywords)}")

        matched_locations = self._matched_terms(searchable_text, profile.locations)
        if matched_locations:
            score += LOCATION_MATCH_SCORE
            reasons.append(f"Matched location: {', '.join(matched_locations)}")

        matched_experience = self._matched_terms(searchable_text, profile.experience_levels)
        if matched_experience:
            score += EXPERIENCE_MATCH_SCORE
            reasons.append(f"Matched experience: {', '.join(matched_experience)}")

        matched = score >= MINIMUM_MATCH_SCORE
        match_level = self.get_match_level(score)

        return JobMatchResult(
            job=job,
            matched=matched,
            score=score,
            match_level=match_level,
            reasons=reasons,
        )

    def get_match_level(self, score: int) -> str:
        if score >= EXCELLENT_MATCH_SCORE:
            return "EXCELLENT MATCH"

        if score >= STRONG_MATCH_SCORE:
            return "STRONG MATCH"

        if score >= MINIMUM_MATCH_SCORE:
            return "MATCH"

        return "NO MATCH"

    def _build_searchable_text(self, job: Job) -> str:
        parts = [
            job.title,
            job.company,
            job.location,
            job.department,
            job.content,
        ]

        return " ".join(part for part in parts if part).lower()

    def _contains_any(self, text: str, terms: list[str]) -> bool:
        return any(term.lower() in text for term in terms)

    def _matched_terms(self, text: str, terms: list[str]) -> list[str]:
        return [term for term in terms if term.lower() in text]