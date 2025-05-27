from app.db.base import Base
from sqlalchemy import Enum as SQLAlchemyEnum, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from datetime import datetime
import enum
from app.models.wallet import Wallet  # Ensure Wallet is imported for relationship


class WalletTransactionType(enum.Enum):  # Use standard enum.Enum
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"
    SPEND = "spend"


class WalletTransactionStatus(enum.Enum):  # Use standard enum.Enum
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"


class WalletTransaction(Base):
    __tablename__ = "wallet_transactions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    wallet_id: Mapped[int] = mapped_column(ForeignKey("wallets.id"), nullable=False)
    amount: Mapped[int] = mapped_column(nullable=False)
    stripe_payment_intent_id: Mapped[str | None] = mapped_column(
        nullable=True, unique=True, index=True
    )

    wallet_transaction_type: Mapped[WalletTransactionType] = mapped_column(
        SQLAlchemyEnum(WalletTransactionType, native_enum=True), nullable=False
    )

    wallet_transaction_status: Mapped[WalletTransactionStatus] = mapped_column(
        SQLAlchemyEnum(WalletTransactionStatus, native_enum=True),
        nullable=False,
        default=WalletTransactionStatus.PENDING,
    )

    created_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
    wallet: Mapped["Wallet"] = relationship(
        back_populates="wallet_transactions", uselist=False
    )
