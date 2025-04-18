from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base
from fastapi_users_db_sqlalchemy import generics
from app.db.models.product import Product

class Character(Base):
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True, autoincrement=True)
    display_id = Column(generics.GUID, index=True, nullable=False)
    name = Column(String(255), index=True, nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    character_images = relationship("CharacterImage", back_populates="character")
    product = relationship("Product", back_populates="characters")
    user = relationship("User", secondary=Product.__tablename__, back_populates="characters", viewonly=True)
