from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from app.db.base import Base
from app.models.oauth_account import OAuthAccount
from sqlalchemy import Boolean, Integer, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List
from datetime import datetime
from typing import TYPE_CHECKING
from app.models.mixin.timestamp import TimestampMixin

if TYPE_CHECKING:
    from app.models.user_wallet import UserWallet
    from app.models.user_api_key import UserApiKey
    from app.models.user_organization_assignment import UserOrganizationAssignment
    from app.models.user_organization_invitation import UserOrganizationInvitation
    from app.models.organization import Organization
    from app.models.organization_api_key import OrganizationApiKey
    from app.models.user_address import UserAddress


class User(SQLAlchemyBaseUserTableUUID, TimestampMixin, Base):
    __tablename__ = "users"

    failed_attempts: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    last_attempted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), default=None, nullable=True
    )
    is_locked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    locked_until: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), default=None, nullable=True
    )
    oauth_accounts: Mapped[List[OAuthAccount]] = relationship(
        "OAuthAccount", lazy="joined"
    )
    user_wallet: Mapped["UserWallet"] = relationship(
        back_populates="user", uselist=False, cascade="all, delete-orphan"
    )
    user_api_keys: Mapped[List["UserApiKey"]] = relationship(
        "UserApiKey", back_populates="user", cascade="all, delete-orphan"
    )
    user_organization_assignments: Mapped[List["UserOrganizationAssignment"]] = (
        relationship(
            "UserOrganizationAssignment",
            back_populates="user",
            cascade="all, delete-orphan",
        )
    )
    user_organization_invitations: Mapped[List["UserOrganizationInvitation"]] = (
        relationship(
            "UserOrganizationInvitation",
            back_populates="user",
            cascade="all, delete-orphan",
            foreign_keys="[UserOrganizationInvitation.user_id]",
        )
    )
    user_organization_invitations_though_created_by: Mapped[
        List["UserOrganizationInvitation"]
    ] = relationship(
        "UserOrganizationInvitation",
        back_populates="created_by_user",
        cascade="all, delete-orphan",
        foreign_keys="[UserOrganizationInvitation.created_by_user_id]",
    )
    organization: Mapped["Organization"] = relationship(
        "Organization", back_populates="created_by_user", uselist=False
    )
    organization_api_keys_though_created_by: Mapped[List["OrganizationApiKey"]] = (
        relationship(
            "OrganizationApiKey",
            back_populates="created_by_user",
            cascade="all, delete-orphan",
            foreign_keys="[OrganizationApiKey.created_by_user_id]",
        )
    )
    address: Mapped["UserAddress"] = relationship(
        "UserAddress",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )
