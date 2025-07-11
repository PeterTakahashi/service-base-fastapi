from app.db.base import Base
from sqlalchemy import ForeignKey, DateTime, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import TYPE_CHECKING
from app.models.mixin.timestamp import TimestampMixin

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.organization import Organization


class UserOrganizationAssignment(TimestampMixin, Base):
    __tablename__ = "user_organization_assignments"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False
    )
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    user: Mapped["User"] = relationship(
        "User", back_populates="user_organization_assignments"
    )
    organization: Mapped["Organization"] = relationship(
        "Organization", back_populates="user_organization_assignments"
    )

    __table_args__ = (
        Index(
            "uq_user_organization_assignment_active",
            "user_id",
            "organization_id",
            unique=True,
            postgresql_where=(deleted_at.is_(None)),
        ),
    )
