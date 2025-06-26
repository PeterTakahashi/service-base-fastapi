# app/models/mixin/wallet_transaction.py
from sqlalchemy import Numeric, Enum as SQLAlchemyEnum
from sqlalchemy.orm import Mapped, mapped_column
from decimal import Decimal
from app.models.enums.wallet_transaction import (
    WalletTransactionType,
    WalletTransactionStatus,
)


class WalletTransactionMixin:
    amount: Mapped[Decimal] = mapped_column(
        Numeric(precision=38, scale=9, asdecimal=True, decimal_return_scale=True),
        default=Decimal("0"),
        nullable=False,
    )
    amount_inclusive_tax: Mapped[Decimal] = mapped_column(
        Numeric(precision=38, scale=9, asdecimal=True, decimal_return_scale=True),
        default=Decimal("0"),
        nullable=True,
    )
    balance_after_transaction: Mapped[Decimal] = mapped_column(
        Numeric(precision=38, scale=9, asdecimal=True, decimal_return_scale=True),
        default=Decimal("0"),
        nullable=True,
    )
    stripe_payment_intent_id: Mapped[str | None] = mapped_column(
        nullable=True, unique=True, index=True
    )
    wallet_transaction_type: Mapped[WalletTransactionType] = mapped_column(
        SQLAlchemyEnum(WalletTransactionType, native_enum=True),
        nullable=False,
        default=WalletTransactionType.DEPOSIT,
    )
    wallet_transaction_status: Mapped[WalletTransactionStatus] = mapped_column(
        SQLAlchemyEnum(WalletTransactionStatus, native_enum=True),
        nullable=False,
        default=WalletTransactionStatus.PENDING,
    )
