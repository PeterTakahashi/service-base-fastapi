from fastapi_users import schemas
from pydantic import EmailStr, Field


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
