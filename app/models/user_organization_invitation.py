from app.db.base import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from sqlalchemy import Uuid
from app.models.mixin.timestamp import TimestampMixin

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.organization import Organization


class UserOrganizationInvitation(TimestampMixin, Base):
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
