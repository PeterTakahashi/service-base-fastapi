from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base
from fastapi_users_db_sqlalchemy import generics
from app.db.models.product import Product

class Episode(Base):
    __tablename__ = "episodes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    display_id = Column(generics.GUID, index=True, nullable=False)
    title = Column(String(255), index=True, nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    pages = relationship("Page", back_populates="episode")
    product = relationship("Product", back_populates="episodes")
    user = relationship("User", secondary=Product.__tablename__, back_populates="episodes", viewonly=True)
