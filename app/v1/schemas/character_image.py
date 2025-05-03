from typing import Optional
from pydantic import Field, field_serializer
from app.v1.schemas.base import HasEncodedID
from app.core.s3 import generate_presigned_url

class CharacterImageRead(HasEncodedID):
    image_url: Optional[str] = ""
    storage_key: Optional[str] = Field(default=None, exclude=True)

    @field_serializer("image_url")
    def serialize_image_url(self, value: Optional[str]) -> str:
        return generate_presigned_url(self.storage_key)
