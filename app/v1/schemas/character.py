from datetime import datetime
from app.v1.schemas.base import HasEncodedID, IDField
from .character_image import CharacterImageRead
from typing import List
from app.lib.convert_id import encode_id
from pydantic import field_serializer

class CharacterRead(HasEncodedID):
    name: str
    created_at: datetime
    updated_at: datetime
    character_images: List[CharacterImageRead]
    product_id: int = IDField
    @field_serializer("product_id")
    def serialize_product_id(self, value: int) -> str:
        return encode_id(value)
