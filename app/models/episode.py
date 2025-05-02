from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.base import Base, TimestampMixin
from app.models.product import Product

class Episode(TimestampMixin, Base):
    __tablename__ = "episodes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), index=True, nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)

    pages = relationship("Page", back_populates="episode")
    product = relationship("Product", back_populates="episodes")
    user = relationship(
        "User",
        secondary=Product.__tablename__,
        back_populates="episodes",
        viewonly=True,
    )

    __table_args__ = (
        UniqueConstraint("title", "product_id", name="uq_title_product_id"),
    )
