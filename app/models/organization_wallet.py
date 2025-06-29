from app.db.base import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List

from app.models.mixin.timestamp import TimestampMixin
from app.models.mixin.wallet import WalletMixin

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.organization import Organization
    from app.models.organization_wallet_transaction import OrganizationWalletTransaction


class OrganizationWallet(TimestampMixin, WalletMixin, Base):
    __tablename__ = "organization_wallets"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.id"), nullable=False, unique=True, index=True
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
