from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, DateTime
from datetime import datetime, timezone
from typing import Optional

Base = declarative_base()


class TimestampMixin:
    deleted_at: Optional[datetime] = Column(DateTime(timezone=True), nullable=True, default=None)
    created_at: datetime = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at: datetime = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
