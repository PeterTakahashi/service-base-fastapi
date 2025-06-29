from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime


class ApiKeyMixin:
    name: Mapped[str] = mapped_column(String, nullable=False)
    api_key: Mapped[str] = mapped_column(
        String, unique=True, index=True, nullable=False
    )
    expires_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    allowed_origin: Mapped[str | None] = mapped_column(String, nullable=True)
    allowed_ip: Mapped[str | None] = mapped_column(String, nullable=True)
