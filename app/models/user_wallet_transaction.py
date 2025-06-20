from app.db.base import Base
from sqlalchemy import Enum as SQLAlchemyEnum, ForeignKey, DateTime, func, Numeric
from sqlalchemy.orm import mapped_column, Mapped, relationship
from datetime import datetime
from app.models.enums.wallet_transaction import (
    WalletTransactionType,
    WalletTransactionStatus,
)
from decimal import Decimal

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user_wallet import UserWallet


class UserWalletTransaction(Base):
    __tablename__ = "user_wallet_transactions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_wallet_id: Mapped[int] = mapped_column(
        ForeignKey("user_wallets.id"), nullable=False
    )
    amount: Mapped[Decimal] = mapped_column(
        Numeric(precision=38, scale=9, asdecimal=True),
        default=Decimal("0"),
        nullable=False,
    )
    stripe_payment_intent_id: Mapped[str | None] = mapped_column(
        nullable=True, unique=True, index=True
    )

    user_wallet_transaction_type: Mapped[WalletTransactionType] = mapped_column(
        SQLAlchemyEnum(WalletTransactionType, native_enum=True),
        nullable=False,
        default=WalletTransactionType.DEPOSIT,
    )

    user_wallet_transaction_status: Mapped[WalletTransactionStatus] = mapped_column(
        SQLAlchemyEnum(WalletTransactionStatus, native_enum=True),
        nullable=False,
        default=WalletTransactionStatus.PENDING,
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
    user_wallet: Mapped["UserWallet"] = relationship(
        back_populates="user_wallet_transactions", uselist=False
    )
