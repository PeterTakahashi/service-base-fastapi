from pydantic import BaseModel, Field, ConfigDict, field_serializer
from datetime import datetime
from app.lib.convert_id import encode_id

class ProductRead(BaseModel):
    id: int = Field(
        ...,
        json_schema_extra={"example": "tAg2D2n1"},
        description="The unique identifier of the product."
    )
    title: str = Field(
        ...,
        min_length=1,
        max_length=100,
        json_schema_extra={"example": "My Product Title"},
        description="The title of the product.",
    )
    created_at: datetime
    updated_at: datetime
    episode_count: int = Field(0, alias="episodes_count")

    model_config = ConfigDict(from_attributes=True)

    @field_serializer("id")
    def serialize_id(self, value: int) -> str:
        return encode_id(value)

class ProductModify(BaseModel):
    title: str = Field(
        ...,
        min_length=1,
        max_length=100,
        json_schema_extra={"example": "My Product Title"},
        description="The title of the product.",
    )

class ProductCreate(ProductModify):
    pass


class ProductUpdate(ProductModify):
    pass
