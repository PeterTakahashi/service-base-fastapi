from app.db.base import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from typing import List
from app.models.wallet_transaction import WalletTransaction
from app.models.user import User


class Wallet(Base):
    __tablename__ = "wallets"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    stripe_customer_id: Mapped[str] = mapped_column(
        nullable=False, unique=True, index=True
    )
    balance: Mapped[int] = mapped_column(default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    user: Mapped["User"] = relationship("User", back_populates="wallet")
    transactions: Mapped[List[WalletTransaction]] = relationship(
        "WalletTransaction", back_populates="wallet", cascade="all, delete-orphan"
    )
