from pydantic import BaseModel, Field
from datetime import datetime
from app.v1.schemas.base import HasEncodedID


class ProductRead(HasEncodedID):
    title: str = Field(
        ...,
        min_length=1,
        max_length=100,
        json_schema_extra={"example": "My Product Title"},
        description="The title of the product.",
    )
    created_at: datetime
    updated_at: datetime


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
