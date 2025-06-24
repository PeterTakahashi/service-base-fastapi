from app.db.base import Base
from sqlalchemy import ForeignKey, DateTime, func, Numeric
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from typing import List
from decimal import Decimal

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.organization import Organization
    from app.models.organization_wallet_transaction import OrganizationWalletTransaction


class OrganizationWallet(Base):
    __tablename__ = "organization_wallets"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.id"), nullable=False
    )
    stripe_customer_id: Mapped[str] = mapped_column(
        nullable=False, unique=True, index=True
    )
    balance: Mapped[Decimal] = mapped_column(
        Numeric(precision=38, scale=9, asdecimal=True, decimal_return_scale=True),
        default=Decimal("0"),
        nullable=False,
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

    organization: Mapped["Organization"] = relationship(
        "Organization", back_populates="organization_wallet", uselist=False
    )
    organization_wallet_transactions: Mapped[List["OrganizationWalletTransaction"]] = relationship(
        "OrganizationWalletTransaction",
        back_populates="organization_wallet",
        cascade="all, delete-orphan",
    )
