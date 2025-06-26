from datetime import datetime
from pydantic import Field, EmailStr, ConfigDict
from app.v1.schemas.common.id_encoder import HasEncodedID
from app.v1.schemas.user import UserRead
from app.v1.schemas.common.address.read import AddressRead


class OrganizationRead(HasEncodedID):
    name: str = Field(..., description="Organization name.")
    description: str | None = Field(None, description="Organization description.")
    profile_image_key: str | None = Field(None, description="Profile image object key.")
    billing_email: EmailStr | None = Field(None, description="Billing contact e-mail.")
    created_by_user: UserRead = Field(
        ..., description="User who created the organization."
    )
    address: AddressRead | None = Field(
        None, description="Registered address of the organization."
    )
    created_at: datetime = Field(..., description="Record creation timestamp.")
    updated_at: datetime = Field(..., description="Record update timestamp.")

    model_config = ConfigDict(from_attributes=True)
