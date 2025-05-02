from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.base import Base, TimestampMixin
from fastapi_users_db_sqlalchemy import generics
from app.models.product import Product
from uuid import uuid4

class Character(TimestampMixin, Base):
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), index=True, nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)

    character_images = relationship("CharacterImage", back_populates="character")
    product = relationship("Product", back_populates="characters")
    user = relationship(
        "User",
        secondary=Product.__tablename__,
        back_populates="characters",
        viewonly=True,
    )

    __table_args__ = (
        UniqueConstraint("name", "product_id", name="uq_name_product_id"),
    )
