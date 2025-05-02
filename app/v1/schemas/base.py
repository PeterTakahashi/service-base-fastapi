from pydantic import BaseModel, Field, field_serializer, ConfigDict
from app.lib.convert_id import encode_id

class HasEncodedID(BaseModel):
    id: int = Field(
        ...,
        json_schema_extra={"example": "jAg2Dqn1"},
        description="The ID of the object",
    )

    @field_serializer("id")
    def serialize_id(self, value: int) -> str:
        return encode_id(value)

    model_config = ConfigDict(from_attributes=True)