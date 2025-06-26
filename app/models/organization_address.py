from typing import TYPE_CHECKING
from app.db.base import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.mixin.address import AddressMixin
from app.models.mixin.timestamp import TimestampMixin

if TYPE_CHECKING:
    from app.models.organization import Organization


class OrganizationAddress(AddressMixin, TimestampMixin, Base):
    __tablename__ = "organization_addresses"

    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        unique=True,
    )

    # back-populates は Organization 側で定義
    organization: Mapped["Organization"] = relationship(
        "Organization", back_populates="address", uselist=False
    )
