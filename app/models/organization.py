from app.db.base import Base
from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user_organization_assignment import UserOrganizationAssignment


class Organization(Base):
    __tablename__ = "organizations"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    profile_image_key: Mapped[str] = mapped_column(String, nullable=True)
    billing_email: Mapped[str] = mapped_column(String, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    user_assignments: Mapped[List["UserOrganizationAssignment"]] = relationship(
        "UserOrganizationAssignment",
        back_populates="organization",
        cascade="all, delete-orphan",
    )
