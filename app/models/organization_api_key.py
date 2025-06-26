from app.db.base import Base
from sqlalchemy import ForeignKey, String, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from sqlalchemy import Uuid
from typing import TYPE_CHECKING
from app.models.mixin.timestamp import TimestampMixin

if TYPE_CHECKING:
    from app.models.organization import Organization
    from app.models.user import User


class OrganizationApiKey(TimestampMixin, Base):
    __tablename__ = "organization_api_keys"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    api_key: Mapped[str] = mapped_column(
        String, unique=True, index=True, nullable=False
    )
    organization_id: Mapped[Uuid] = mapped_column(
        ForeignKey("organizations.id"), nullable=False
    )
    expires_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    allowed_origin: Mapped[str | None] = mapped_column(String, nullable=True)
    allowed_ip: Mapped[str | None] = mapped_column(String, nullable=True)

    created_by_user_id: Mapped[Uuid] = mapped_column(
        ForeignKey("users.id"), nullable=False
    )
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    organization: Mapped["Organization"] = relationship(
        "Organization", back_populates="organization_api_keys"
    )
    created_by_user: Mapped["User"] = relationship("User")
