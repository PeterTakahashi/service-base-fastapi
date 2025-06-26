from app.db.base import Base
from sqlalchemy import ForeignKey, String, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from sqlalchemy import Uuid
from app.models.mixin.timestamp import TimestampMixin

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User


class UserApiKey(TimestampMixin, Base):
    __tablename__ = "user_api_keys"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    api_key: Mapped[str] = mapped_column(
        String, unique=True, index=True, nullable=False
    )
    user_id: Mapped[Uuid] = mapped_column(ForeignKey("users.id"), nullable=False)
    expires_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    allowed_origin: Mapped[str | None] = mapped_column(String, nullable=True)
    allowed_ip: Mapped[str | None] = mapped_column(String, nullable=True)
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    user: Mapped["User"] = relationship("User", back_populates="user_api_keys")
