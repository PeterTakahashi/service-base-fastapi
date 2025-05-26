from app.db.base import Base
from sqlalchemy import Enum as SQLAlchemyEnum, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped
from datetime import datetime
import enum


class TransactionType(enum.Enum):  # Use standard enum.Enum
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"
    SPEND = "spend"


class TransactionStatus(enum.Enum):  # Use standard enum.Enum
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

    transaction_type: Mapped[TransactionType] = mapped_column(
        SQLAlchemyEnum(TransactionType, native_enum=True), nullable=False
    )

    status: Mapped[TransactionStatus] = mapped_column(
        SQLAlchemyEnum(TransactionStatus, native_enum=True),
        nullable=False,
        default=TransactionStatus.PENDING,
    )

    created_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
