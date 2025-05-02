from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship
from app.db.base import Base, TimestampMixin
from fastapi_users_db_sqlalchemy import generics
from uuid import uuid4

class CharacterImage(TimestampMixin, Base):
    __tablename__ = "character_images"

    id = Column(Integer, primary_key=True, autoincrement=True)
    character_id = Column(
        Integer, ForeignKey("characters.id"), nullable=False, index=True
    )

    character = relationship("Character", back_populates="character_images")
