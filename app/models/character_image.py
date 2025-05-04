from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampMixin
from typing import Optional

class CharacterImage(TimestampMixin, Base):
    __tablename__ = "character_images"

    id = Column(Integer, primary_key=True, autoincrement=True)
    character_id = Column(
        Integer, ForeignKey("characters.id"), nullable=False, index=True
    )
    storage_key: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    character = relationship("Character", back_populates="character_images")
