from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


class AddressMixin:
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # --- Stripe 互換フィールド -----------------------------
    city: Mapped[str] = mapped_column(String, nullable=False)
    country: Mapped[str] = mapped_column(String(2), nullable=False)  # ISO-3166-1 α-2
    line1: Mapped[str] = mapped_column(String, nullable=False)
    line2: Mapped[str | None] = mapped_column(String, nullable=True)
    postal_code: Mapped[str] = mapped_column(String, nullable=False)
    state: Mapped[str] = mapped_column(String, nullable=False)  # ISO-3166-2
    # --------------------------------------------------------
