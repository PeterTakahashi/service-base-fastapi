from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from app.db.base import Base
from app.models.oauth_account import OAuthAccount
from sqlalchemy import Boolean, Integer, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.wallet import Wallet
    from app.models.user_api_keys import UserApiKey


class User(SQLAlchemyBaseUserTableUUID, Base):
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
    wallet: Mapped["Wallet"] = relationship(back_populates="user", uselist=False)
    user_api_keys: Mapped[List["UserApiKey"]] = relationship(
        "UserApiKey", back_populates="user", cascade="all, delete-orphan"
    )
