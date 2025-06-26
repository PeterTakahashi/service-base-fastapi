from fastapi_users import schemas
from pydantic import EmailStr, ConfigDict
from typing import Generic
from fastapi_users import models


class UserRead(schemas.CreateUpdateDictModel, Generic[models.ID]):
    id: models.ID
    email: EmailStr
    is_verified: bool = False
    model_config = ConfigDict(from_attributes=True)
