from app.db.base import Base
from sqlalchemy import ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import Uuid

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.organization import Organization


class UserOrganizationInvitation(Base):
    __tablename__ = "user_organization_invitations"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[Uuid] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True
    )
    created_by_user_id: Mapped[Uuid] = mapped_column(
        ForeignKey("users.id"), nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    user: Mapped["User"] = relationship(
        "User", back_populates="user_organization_invitations", foreign_keys=[user_id]
    )
    organization: Mapped["Organization"] = relationship(
        "Organization", back_populates="user_organization_invitations"
    )
    created_by_user: Mapped["User"] = relationship(
        "User",
        back_populates="user_organization_invitations_though_created_by",
        foreign_keys=[created_by_user_id],
    )
