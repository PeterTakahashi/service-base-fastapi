from datetime import datetime
from app.v1.schemas.base import HasEncodedID
from .character_image import CharacterImageRead
from typing import List
from pydantic import Field

class CharacterRead(HasEncodedID):
    name: str
    created_at: datetime
    updated_at: datetime
    product_id: int
    character_images: List[CharacterImageRead]
