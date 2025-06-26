from fastapi_users import schemas
from pydantic import EmailStr, ConfigDict, Field
from typing import Generic
from fastapi_users import models
from app.v1.schemas.user_address import UserAddressRead


class UserRead(schemas.CreateUpdateDictModel, Generic[models.ID]):
    id: models.ID
    email: EmailStr
    is_verified: bool = False
    address: UserAddressRead | None = Field(
        None,
        description="Registered address of the user.",
    )
    model_config = ConfigDict(from_attributes=True)
