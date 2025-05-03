from typing import Optional
from app.v1.schemas.base import HasEncodedID
from pydantic import field_serializer

class CharacterImageRead(HasEncodedID):
    image_url: Optional[str] = ""
    storage_key: Optional[str] = None

    @field_serializer("image_url")
    def serialize_image_url(self, value: Optional[str]) -> str:
        if self.storage_key is None:
            return ""
        return generate_presigned_url(self.storage_key)