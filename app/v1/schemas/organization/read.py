from datetime import datetime
from pydantic import Field, EmailStr, ConfigDict
from app.v1.schemas.common.id_encoder import HasEncodedID


class OrganizationRead(HasEncodedID):
    name: str = Field(..., description="Organization name.")
    profile_image_key: str | None = Field(None, description="Profile image object key.")
    billing_email: EmailStr | None = Field(None, description="Billing contact e-mail.")
    created_at: datetime = Field(..., description="Record creation timestamp.")
    updated_at: datetime = Field(..., description="Record update timestamp.")

    model_config = ConfigDict(from_attributes=True)
