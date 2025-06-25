from app.db.base import Base
from sqlalchemy import ForeignKey, String, DateTime, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from sqlalchemy import Uuid
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.organization import Organization
    from app.models.user import User


class OrganizationApiKey(Base):
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
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
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

    organization: Mapped["Organization"] = relationship(
        "Organization", back_populates="organization_api_keys"
    )
    created_by_user: Mapped["User"] = relationship("User")
