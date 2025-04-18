from sqlalchemy import Column, ForeignKey, String, DateTime, Integer
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db.base import Base
from fastapi_users_db_sqlalchemy import generics

class CharacterImage(Base):
    __tablename__ = "character_images"

    id = Column(Integer, primary_key=True, autoincrement=True)
    display_id = Column(generics.GUID, index=True, nullable=False)
    character_id = Column(Integer, ForeignKey("characters.id"), nullable=False, index=True)
    image_url = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    character = relationship("Character", back_populates="character_images")
