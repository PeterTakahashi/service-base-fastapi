from app.db.base import Base
from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from sqlalchemy import Uuid
from typing import TYPE_CHECKING
from app.models.mixin.timestamp import TimestampMixin
from app.models.mixin.api_key import ApiKeyMixin

if TYPE_CHECKING:
    from app.models.organization import Organization
    from app.models.user import User

API_KEY_PREFIX = "organization_"


class OrganizationApiKey(TimestampMixin, ApiKeyMixin, Base):
    __tablename__ = "organization_api_keys"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    organization_id: Mapped[Uuid] = mapped_column(
        ForeignKey("organizations.id"), nullable=False
    )
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
