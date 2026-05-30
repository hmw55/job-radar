from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base



class JobNotification(Base):
    __tablename__ = "job_notifications"

    __table_args__ = (
        UniqueConstraint(
            "job_id",
            "profile_name",
            "channel",
            name="uq_job_notifications_job_profile_channel",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    job_id: Mapped[int] = mapped_column(ForeignKey("jobs.id"), nullable=False)
    profile_name: Mapped[str] = mapped_column(String(255), nullable=False)
    channel: Mapped[str] = mapped_column(String(100), nullable=False)

    sent_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )