from app.db.base import Base
from sqlalchemy import Enum as SQLAlchemyEnum, ForeignKey, Numeric
from sqlalchemy.orm import mapped_column, Mapped, relationship
from app.models.enums.wallet_transaction import (
    WalletTransactionType,
    WalletTransactionStatus,
)
from decimal import Decimal
from app.models.mixin.timestamp import TimestampMixin

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.organization_wallet import OrganizationWallet


class OrganizationWalletTransaction(TimestampMixin, Base):
    __tablename__ = "organization_wallet_transactions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    organization_wallet_id: Mapped[int] = mapped_column(
        ForeignKey("organization_wallets.id"), nullable=False
    )
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
    organization_wallet: Mapped["OrganizationWallet"] = relationship(
        back_populates="organization_wallet_transactions", uselist=False
    )
