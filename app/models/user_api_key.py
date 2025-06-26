from app.db.base import Base
from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from sqlalchemy import Uuid
from app.models.mixin.timestamp import TimestampMixin
from app.models.mixin.api_key import ApiKeyMixin

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User

API_KEY_PREFIX = "user_"


class UserApiKey(TimestampMixin, ApiKeyMixin, Base):
    __tablename__ = "user_api_keys"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[Uuid] = mapped_column(ForeignKey("users.id"), nullable=False)
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    user: Mapped["User"] = relationship("User", back_populates="user_api_keys")
