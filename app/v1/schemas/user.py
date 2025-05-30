from fastapi_users import schemas
from pydantic import EmailStr, ConfigDict, Field
from typing import Generic, Optional
from fastapi_users import models
from app.v1.schemas.wallet import WalletRead


class UserRead(schemas.CreateUpdateDictModel, Generic[models.ID]):
    id: models.ID
    email: EmailStr
    is_verified: bool = False
    model_config = ConfigDict(from_attributes=True)


class UserWithWalletRead(UserRead):
    wallet: WalletRead = Field(
        description="The wallet associated with the user.",
    )


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
        default=None,
        max_length=320,
        json_schema_extra={"example": "user@example.com"},
        description="The email of the user.",
    )
    password: Optional[str] = Field(
        default=None,
        min_length=8,
        max_length=100,
        json_schema_extra={"example": "password123%"},
        description="The password of the user.",
    )
