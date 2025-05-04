from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base, TimestampMixin
from app.models.types.enum_types import EnumIntegerType
from enum import Enum


class StatusEnum(Enum):
    DRAFT = 0
    PENDING = 1
    DETECTION = 2
    OCR = 3
    TRANSLATION = 4
    UPSCALING = 5
    MASK_GENERATION = 6
    INPAINTING = 7
    RENDERING = 8
    FINISHED = 9


class Page(TimestampMixin, Base):
    __tablename__ = "pages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    episode_id = Column(
        Integer,
        ForeignKey("episodes.id"),
        nullable=False,
        index=True)
    translation_status: Column = Column(
        EnumIntegerType(StatusEnum), default=StatusEnum.DRAFT, nullable=False
    )
    before_changed_image_storage_key = Column(String(255), nullable=False)
    after_changed_image_storage_key = Column(String(255), nullable=False)

    episode = relationship("Episode", back_populates="pages")
