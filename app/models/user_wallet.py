from app.db.base import Base
from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List
import fastapi_users_db_sqlalchemy
from decimal import Decimal
from app.models.mixin.timestamp import TimestampMixin

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.user_wallet_transaction import UserWalletTransaction


class UserWallet(TimestampMixin, Base):
    __tablename__ = "user_wallets"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[fastapi_users_db_sqlalchemy.generics.GUID] = mapped_column(
        ForeignKey("users.id"), nullable=False
    )
    stripe_customer_id: Mapped[str] = mapped_column(
        nullable=False, unique=True, index=True
    )
    balance: Mapped[Decimal] = mapped_column(
        Numeric(precision=38, scale=9, asdecimal=True, decimal_return_scale=True),
        default=Decimal("0"),
        nullable=False,
    )

    user: Mapped["User"] = relationship(
        "User", back_populates="user_wallet", uselist=False
    )
    user_wallet_transactions: Mapped[List["UserWalletTransaction"]] = relationship(
        "UserWalletTransaction",
        back_populates="user_wallet",
        cascade="all, delete-orphan",
    )
