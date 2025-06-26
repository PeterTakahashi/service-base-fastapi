from app.db.base import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List
import fastapi_users_db_sqlalchemy
from app.models.mixin.timestamp import TimestampMixin
from app.models.mixin.wallet import WalletMixin

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.user_wallet_transaction import UserWalletTransaction


class UserWallet(TimestampMixin, WalletMixin, Base):
    __tablename__ = "user_wallets"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[fastapi_users_db_sqlalchemy.generics.GUID] = mapped_column(
        ForeignKey("users.id"), nullable=False
    )
    user: Mapped["User"] = relationship(
        "User", back_populates="user_wallet", uselist=False
    )
    user_wallet_transactions: Mapped[List["UserWalletTransaction"]] = relationship(
        "UserWalletTransaction",
        back_populates="user_wallet",
        cascade="all, delete-orphan",
    )
