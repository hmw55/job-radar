from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, Text, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base

class JobMatch(Base):
    __tablename__ = "job matches"

    __table_args__ = (
        UniqueConstraint(
            "job_id",
            "profile_name",
            name="uq_job_matches_job_profile",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    job_id: Mapped[int] = mapped_column(ForeignKey("jobs.id"), nullable=False)
    profile_name: Mapped[str] = mapped_column(String(255), nullable=False)

    score: Mapped[int] = mapped_column(Integer, nullable=False)
    match_level: Mapped[str] = mapped_column(String(100), nullable=False)
    reasons: Mapped[str]= mapped_column(Text, nullable=False)

    matched_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )