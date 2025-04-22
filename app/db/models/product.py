from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base, TimestampMixin
from fastapi_users_db_sqlalchemy import generics
from uuid import uuid4

class Product(TimestampMixin, Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    display_id = Column(generics.GUID, index=True, nullable=False, default=uuid4)
    title = Column(String(255), index=True, nullable=False)
    user_id = Column(generics.GUID, ForeignKey("users.id"), nullable=False, index=True)

    user = relationship("User", back_populates="products")
    episodes = relationship("Episode", back_populates="product")
    characters = relationship("Character", back_populates="product")
