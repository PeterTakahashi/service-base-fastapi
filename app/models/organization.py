from app.db.base import Base
from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import List, TYPE_CHECKING
from sqlalchemy import Uuid
from app.models.mixin.timestamp import TimestampMixin

if TYPE_CHECKING:
    from app.models.organization_wallet import OrganizationWallet
    from app.models.user_organization_assignment import UserOrganizationAssignment
    from app.models.user_organization_invitation import UserOrganizationInvitation
    from app.models.user import User
    from app.models.organization_api_key import OrganizationApiKey
    from app.models.organization_address import OrganizationAddress


class Organization(TimestampMixin, Base):
    __tablename__ = "organizations"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(String, nullable=True, default=None)
    profile_image_key: Mapped[str | None] = mapped_column(
        String, nullable=True, default=None
    )
    billing_email: Mapped[str | None] = mapped_column(
        String, nullable=True, default=None
    )
    tax_type: Mapped[str | None] = mapped_column(String, nullable=True, default=None)
    tax_id: Mapped[str | None] = mapped_column(String, nullable=True, default=None)

    created_by_user_id: Mapped[Uuid] = mapped_column(
        ForeignKey("users.id"), nullable=False
    )
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    user_organization_assignments: Mapped[List["UserOrganizationAssignment"]] = (
        relationship(
            "UserOrganizationAssignment",
            back_populates="organization",
            cascade="all, delete-orphan",
        )
    )
    user_organization_invitations: Mapped[List["UserOrganizationInvitation"]] = (
        relationship(
            "UserOrganizationInvitation",
            back_populates="organization",
            cascade="all, delete-orphan",
        )
    )
    created_by_user: Mapped["User"] = relationship("User")
    organization_wallet: Mapped["OrganizationWallet"] = relationship(
        back_populates="organization", uselist=False
    )
    organization_api_keys: Mapped[List["OrganizationApiKey"]] = relationship(
        "OrganizationApiKey",
        back_populates="organization",
        cascade="all, delete-orphan",
    )
    address: Mapped["OrganizationAddress"] = relationship(
        "OrganizationAddress",
        back_populates="organization",
        uselist=False,
        cascade="all, delete-orphan",
    )
