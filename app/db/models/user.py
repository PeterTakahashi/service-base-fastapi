from datetime import datetime, timezone
from sqlalchemy import Column, DateTime
from sqlalchemy.orm import relationship
from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from app.db.base import Base, TimestampMixin
from app.db.models.product import Product

class User(SQLAlchemyBaseUserTableUUID, TimestampMixin, Base):
    __tablename__ = "users"

    products = relationship("Product", back_populates="user")
    episodes = relationship("Episode", secondary=Product.__tablename__, back_populates="user", viewonly=True)
    characters = relationship("Character", secondary=Product.__tablename__, back_populates="user", viewonly=True)
