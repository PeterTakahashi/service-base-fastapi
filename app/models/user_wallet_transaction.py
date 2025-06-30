from app.db.base import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from app.models.mixin.timestamp import TimestampMixin
from app.models.mixin.wallet_transaction import WalletTransactionMixin

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user_wallet import UserWallet


class UserWalletTransaction(TimestampMixin, WalletTransactionMixin, Base):
    __tablename__ = "user_wallet_transactions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_wallet_id: Mapped[int] = mapped_column(
        ForeignKey("user_wallets.id", ondelete="CASCADE"), nullable=False
    )
    user_wallet: Mapped["UserWallet"] = relationship(
        back_populates="user_wallet_transactions", uselist=False
    )
