from fastapi_users import schemas, models
from pydantic import EmailStr, ConfigDict, Field
from typing import Optional, Generic


class UserRead(schemas.CreateUpdateDictModel, Generic[models.ID]):
    """Base User model."""

    id: models.ID
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)

class UserCreate(schemas.CreateUpdateDictModel):
    email: EmailStr = Field(
        ...,
        max_length=320,
        json_schema_extra={"example": "user@example.com"},
        description="The email of the user.",
    )
    password: str = Field(
        ...,
        min_length=8,
        max_length=100,
        json_schema_extra={"example": "password123%"},
        description="The password of the user.",
    )


class UserUpdate(schemas.CreateUpdateDictModel):
    email: Optional[EmailStr] = Field(
        None,
        max_length=320,
        json_schema_extra={"example": "user@example.com"},
        description="The email of the user.",
    )
    password: Optional[str] = Field(
        None,
        min_length=8,
        max_length=100,
        json_schema_extra={"example": "password123%"},
        description="The password of the user.",
    )
