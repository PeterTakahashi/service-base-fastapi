from sqlalchemy import Numeric
from sqlalchemy.orm import Mapped, mapped_column
from decimal import Decimal


class WalletMixin:
    stripe_customer_id: Mapped[str] = mapped_column(
        nullable=False, unique=True, index=True
    )
    balance: Mapped[Decimal] = mapped_column(
        Numeric(precision=38, scale=9, asdecimal=True, decimal_return_scale=True),
        default=Decimal("0"),
        nullable=False,
    )
