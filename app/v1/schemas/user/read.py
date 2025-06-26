from fastapi_users import schemas
from pydantic import EmailStr, ConfigDict, Field
from typing import Generic
from fastapi_users import models
from app.v1.schemas.common.address.read import AddressRead


class UserRead(schemas.CreateUpdateDictModel, Generic[models.ID]):
    id: models.ID
    email: EmailStr
    is_verified: bool = False
    # address: AddressRead | None = Field(
    #     None,
    #     description="Registered address of the user.",
    #     json_schema_extra={
    #         "example": {
    #             "line1": "123 Main St",
    #             "line2": "Suite 100",
    #             "city": "Metropolis",
    #             "state": "NY",
    #             "postal_code": "12345",
    #             "country": "US",
    #         }
    #     },
    # )
    model_config = ConfigDict(from_attributes=True)
