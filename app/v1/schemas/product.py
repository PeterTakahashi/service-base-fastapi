from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID
from datetime import datetime


class ProductRead(BaseModel):
    id: UUID = Field(..., validation_alias="display_id")
    title: str
    created_at: datetime
    updated_at: datetime
    episode_count: int = Field(0, alias="episodes_count")

    model_config = ConfigDict(from_attributes=True)


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
