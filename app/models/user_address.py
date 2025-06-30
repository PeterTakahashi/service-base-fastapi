from typing import TYPE_CHECKING
from app.db.base import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.mixin.address import AddressMixin
from app.models.mixin.timestamp import TimestampMixin

if TYPE_CHECKING:
    from app.models.user import User


class UserAddress(AddressMixin, TimestampMixin, Base):
    __tablename__ = "user_addresses"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        unique=True,
    )

    user: Mapped["User"] = relationship("User", back_populates="address", uselist=False)
