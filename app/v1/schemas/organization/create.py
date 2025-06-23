from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class OrganizationCreate(BaseModel):
    name: str = Field(
        ...,
        max_length=255,
        description="Organization name.",
        json_schema_extra={"example": "Acme Inc."},
    )
    description: Optional[str] = Field(
        None,
        max_length=1000,
        description="Organization description.",
        json_schema_extra={"example": "A leading provider of innovative solutions."},
    )
    profile_image_key: Optional[str] = Field(
        None,
        description="Key (e.g. S3/MinIO object key) of the profile image.",
        json_schema_extra={"example": "org/1/profile.png"},
    )
    billing_email: Optional[EmailStr] = Field(
        None,
        description="Billing contact e-mail address.",
        json_schema_extra={"example": "billing@acme.com"},
    )
