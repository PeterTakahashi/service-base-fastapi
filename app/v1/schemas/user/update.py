from fastapi_users import schemas
from pydantic import EmailStr, Field
from typing import Optional
from app.v1.schemas.common.address.write import AddressWrite


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
    address: Optional[AddressWrite] = Field(
        None,
        description="Registered address of the user.",
        json_schema_extra={
            "example": {
                "line1": "123 Main St",
                "line2": "Suite 100",
                "city": "Metropolis",
                "state": "NY",
                "postal_code": "12345",
                "country": "US",
            }
        },
    )

    def create_update_dict(self):
        return schemas.model_dump(
            self,
            exclude_unset=True,
            exclude={
                "id",
                "is_superuser",
                "is_active",
                "is_verified",
                "oauth_accounts",
                "address",
            },
        )

    def create_update_dict_superuser(self):
        return schemas.model_dump(self, exclude_unset=True, exclude={"id", "address"})
