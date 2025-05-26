from app.db.base import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from typing import List
from app.models.wallet_transaction import WalletTransaction
from app.models.user import User
import fastapi_users_db_sqlalchemy

class Wallet(Base):
    __tablename__ = "wallets"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[fastapi_users_db_sqlalchemy.generics.GUID()] = mapped_column(ForeignKey("users.id"), nullable=False)
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

    user: Mapped["User"] = relationship("User", back_populates="wallet", uselist=False)
    wallet_transactions: Mapped[List[WalletTransaction]] = relationship(
        "WalletTransaction", back_populates="wallet", cascade="all, delete-orphan"
    )
