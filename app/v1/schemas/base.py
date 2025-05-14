from pydantic import BaseModel, Field, field_serializer, ConfigDict
from app.lib.convert_id import encode_id

IDField = Field(
    ...,
    json_schema_extra={"example": "abcd1234xyzc"},
    description="The ID of the object",
)


class HasEncodedID(BaseModel):
    id: int = IDField

    @field_serializer("id")
    def serialize_id(self, value: int) -> str:
        return encode_id(value)

    model_config = ConfigDict(from_attributes=True)
