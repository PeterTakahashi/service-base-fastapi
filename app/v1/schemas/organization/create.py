from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from app.v1.schemas.common.address.write import AddressWrite


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
    address: AddressWrite = Field(
        ...,
        description="Registered address of the organization.",
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
    tax_type: Optional[str] = Field(
        None,
        description="Tax type (e.g., eu_vat) for the organization. ref: https://docs.stripe.com/api/tax_ids/object",
        json_schema_extra={"example": "VAT"},
    )
    tax_id: Optional[str] = Field(
        None,
        description="Tax ID (e.g., VAT number).",
        json_schema_extra={"example": "VAT123456789"},
    )
