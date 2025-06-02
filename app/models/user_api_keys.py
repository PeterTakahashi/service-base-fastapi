from app.db.base import Base
from sqlalchemy import ForeignKey, String, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from sqlalchemy import Uuid
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User


class UserApiKey(Base):
    __tablename__ = "user_api_keys"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    api_key: Mapped[str] = mapped_column(
        String, unique=True, index=True, nullable=False
    )
    user_id: Mapped[Uuid] = mapped_column(ForeignKey("users.id"), nullable=False)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    allowed_origin: Mapped[str | None] = mapped_column(String, nullable=True)
    allowed_ip: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="user_api_keys")
