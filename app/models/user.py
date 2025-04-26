from sqlalchemy.orm import relationship
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from app.db.base import Base
from app.models.product import Product

class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "users"

    products = relationship("Product", back_populates="user")
    episodes = relationship("Episode", secondary=Product.__tablename__, back_populates="user", viewonly=True)
    characters = relationship("Character", secondary=Product.__tablename__, back_populates="user", viewonly=True)
