from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class CompanySource(Base):
    __tablename__ = "company_sources"

    __table_args__ = (
        UniqueConstraint(
            "provider",
            "identifier",
            name="uq_company_sources_provider_identifier",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    provider: Mapped[str] = mapped_column(String(100), nullable=False)
    identifier: Mapped[str] = mapped_column(String(255), nullable=False)
    display_name: Mapped[str] = mapped_column(String(255), nullable=False)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    last_checked_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )