from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.base import Base, TimestampMixin
from fastapi_users_db_sqlalchemy import generics

class Product(TimestampMixin, Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    user_id = Column(generics.GUID, ForeignKey("users.id"), nullable=False, index=True)

    user = relationship("User", back_populates="products")
    episodes = relationship("Episode", back_populates="product")
    characters = relationship("Character", back_populates="product")

    __table_args__ = (
        UniqueConstraint("title", "user_id", name="uq_title_user_id"),
    )
