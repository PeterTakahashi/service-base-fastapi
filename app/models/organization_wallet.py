from app.db.base import Base
from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List
from decimal import Decimal

from app.models.mixin.timestamp import TimestampMixin

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.organization import Organization
    from app.models.organization_wallet_transaction import OrganizationWalletTransaction


class OrganizationWallet(TimestampMixin, Base):
    __tablename__ = "organization_wallets"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.id"), nullable=False, unique=True, index=True
    )
    stripe_customer_id: Mapped[str] = mapped_column(
        nullable=False, unique=True, index=True
    )
    balance: Mapped[Decimal] = mapped_column(
        Numeric(precision=38, scale=9, asdecimal=True, decimal_return_scale=True),
        default=Decimal("0"),
        nullable=False,
    )
    organization: Mapped["Organization"] = relationship(
        "Organization", back_populates="organization_wallet", uselist=False
    )
    organization_wallet_transactions: Mapped[List["OrganizationWalletTransaction"]] = (
        relationship(
            "OrganizationWalletTransaction",
            back_populates="organization_wallet",
            cascade="all, delete-orphan",
        )
    )
