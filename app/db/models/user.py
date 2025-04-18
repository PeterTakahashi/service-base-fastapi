from datetime import datetime, timezone
from sqlalchemy import Column, DateTime
from sqlalchemy.orm import relationship
from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from app.db.base import Base
from app.db.models.product import Product

class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "users"

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    products = relationship("Product", back_populates="user")
    episodes = relationship("Episode", secondary=Product.__tablename__, back_populates="user", viewonly=True)
    characters = relationship("Character", secondary=Product.__tablename__, back_populates="user", viewonly=True)
