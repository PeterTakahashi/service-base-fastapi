from sqlalchemy import Column, ForeignKey, String, Integer
from sqlalchemy.orm import relationship
from app.db.base import Base, TimestampMixin
from fastapi_users_db_sqlalchemy import generics

class CharacterImage(TimestampMixin, Base):
    __tablename__ = "character_images"

    id = Column(Integer, primary_key=True, autoincrement=True)
    display_id = Column(generics.GUID, index=True, nullable=False)
    character_id = Column(Integer, ForeignKey("characters.id"), nullable=False, index=True)
    image_url = Column(String(255), nullable=False)

    character = relationship("Character", back_populates="character_images")
