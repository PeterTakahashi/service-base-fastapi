from pydantic import BaseModel, Field, EmailStr

class OrganizationCreate(BaseModel):
    name: str = Field(
        ...,
        max_length=255,
        description="Organization name.",
        json_schema_extra={"example": "Acme Inc."},
    )
    profile_image_key: str | None = Field(
        None,
        description="Key (e.g. S3/MinIO object key) of the profile image.",
        json_schema_extra={"example": "org/1/profile.png"},
    )
    billing_email: EmailStr | None = Field(
        None,
        description="Billing contact e-mail address.",
        json_schema_extra={"example": "billing@acme.com"},
    )