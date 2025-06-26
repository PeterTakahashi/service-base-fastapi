from app.db.base import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from app.models.mixin.timestamp import TimestampMixin
from app.models.mixin.wallet_transaction import WalletTransactionMixin

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.organization_wallet import OrganizationWallet


class OrganizationWalletTransaction(TimestampMixin, WalletTransactionMixin, Base):
    __tablename__ = "organization_wallet_transactions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    organization_wallet_id: Mapped[int] = mapped_column(
        ForeignKey("organization_wallets.id"), nullable=False
    )
    organization_wallet: Mapped["OrganizationWallet"] = relationship(
        back_populates="organization_wallet_transactions", uselist=False
    )
