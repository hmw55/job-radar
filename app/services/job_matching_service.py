# ============================================================
# Job Matching Engine
# ============================================================
#
# This file contains the core matching logic used by Job Radar.
#
# Every discovered job passes through this service.
#
# The matching engine evaluates:
#
# - Job titles
# - Keywords
# - Locations
# - Experience levels
# - Excluded titles
# - Excluded companies
#
# and produces:
#
# - Match score
# - Match level
# - Match reasoning
#
# The resulting score determines whether a job should be
# considered a match and whether it should be sent to the
# notification pipeline.
#
# If you are modifying how Job Radar ranks opportunities,
# this is usually the first file to inspect.
# ============================================================
from dataclasses import dataclass, field

from app.models.job import Job
from app.profiles.search_profile import SearchProfile

# ============================================================
# Match Thresholds
# ============================================================
#
# These values determine how scores are translated into
# human-readable match levels.
#
# Example:
#
# 95 -> EXCELLENT MATCH
# 75 -> STRONG MATCH
# 55 -> MATCH
# 20 -> NO MATCH
MINIMUM_MATCH_SCORE = 50
STRONG_MATCH_SCORE = 70
EXCELLENT_MATCH_SCORE = 90

# ============================================================
# Score Contributions
# ============================================================
#
# These values control how much each signal contributes
# to the overall match score.
#
# Increasing TITLE_MATCH_SCORE makes role titles more
# important.
#
# Increasing KEYWORD_MATCH_SCORE makes skills and
# technologies more important.
#
# Adjust these values carefully, as they directly impact
# notification quality.
TITLE_MATCH_SCORE = 50
KEYWORD_MATCH_SCORE = 10
LOCATION_MATCH_SCORE = 10
EXPERIENCE_MATCH_SCORE = 10
MAX_KEYWORD_SCORE = 40
REMOTE_MATCH_SCORE = 20


@dataclass(frozen=True)
class JobMatchResult:
    # Result returned by the matching engine.
    # 
    # Contains:
    # - Original job
    # - Match status
    # - Numerical score
    # - Human-readable score
    # - Reasons explaining why the score was assigned
    # 
    # These reasons are later surfaced in logs and notifications 
    # to help users understand why a job matched their profile. 
    job: Job
    matched: bool
    score: int
    match_level: str
    reasons: list[str] = field(default_factory=list)


class JobMatchingService:
    def match_job(self, job: Job, profile: SearchProfile) -> JobMatchResult:
        # Evaluate a job against a search profile.
        # 
        # Matching occurs in several stages: 
        # 1. Locating filtering 
        # 2. Exclusing checks
        # 3. Title matching
        # 4. Keyword matching
        # 5. Remote detection
        # 6. Experience matching
        # 7. Score calculation
        # 
        # A valid title match is currently required before a 
        # job can be considered a match. 
        # 
        # Returns: 
        #   JobMatchResult  
        searchable_text = self._build_searchable_text(job)
        title = job.title.lower()
        company = job.company.lower()

        if self._is_excluded_location(job, profile):
            return JobMatchResult(
                job=job,
                matched=False,
                score=0,
                match_level="NO MATCH",
                reasons=["Excluded location"],
            )
        
        if not self._is_allowed_location(job, profile):
            return JobMatchResult(
                job=job,
                matched=False,
                score=0,
                match_level="NO MATCH",
                reasons=["Location not allowed"],
            )

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

        if job.location and self._is_remote_location(job.location.lower()):
            score += REMOTE_MATCH_SCORE
            reasons.append("Remote position")

        matched_locations = self._match_location(job, profile)
        if matched_locations:
            score += LOCATION_MATCH_SCORE
            reasons.append(f"Matched location: {', '.join(matched_locations)}")

        matched_experience = self._matched_terms(searchable_text, profile.experience_levels)
        if matched_experience:
            score += EXPERIENCE_MATCH_SCORE
            reasons.append(f"Matched experience: {', '.join(matched_experience)}")

        # Require at least one matching target role. 
        # 
        # This prevents jobs from matching solely because they 
        # contain overlapping keywords. 
        # 
        # Example: 
        # 
        # A recruiter role mentioning "Python" should not match 
        # a software engineering profile. 
        has_role_alignment = bool(matched_titles)

        matched = score >= MINIMUM_MATCH_SCORE and has_role_alignment
        match_level = self.get_match_level(score if matched else 0)

        return JobMatchResult(
            job=job,
            matched=matched,
            score=score,
            match_level=match_level,
            reasons=reasons,
        )
    
    def _match_location(self, job: Job, profile: SearchProfile) -> list[str]:
        if not job.location: 
            return []
        
        location_text = job.location.lower()
        matches: list[str] = []

        for location in profile.locations:
            normalized_location = location.lower()

            if normalized_location in location_text:
                matches.append(location)

        if self._is_remote_location(location_text) and "remote" not in matches:
            matches.append("remote")

        return matches
    
    def _is_remote_location(self, location_text: str) -> bool:
        remote_terms = [
            "remote",
            "remote -",
            "remote,",
            "anywhere",
            "distributed",
        ]

        return any(term in location_text for term in remote_terms)
    
    def _is_excluded_location(
            self,
            job: Job,
            profile: SearchProfile,
    ) -> bool:
        if not job.location:
            return False
        
        location_text = job.location.lower()

        return any(
            location.lower() in location_text
            for location in profile.excluded_locations
        )
    
    def _is_allowed_location(
            self,  
            job: Job,
            profile: SearchProfile,
    ) -> bool:
        if not job.location:
            return True
        
        location_text = job.location.lower()

        return any(
            location.lower() in location_text
            for location in profile.allowed_locations
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