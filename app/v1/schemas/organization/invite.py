from pydantic import BaseModel, Field, EmailStr


class OrganizationUserInvite(BaseModel):
    email: EmailStr = Field(
        ...,
        max_length=320,
        description="The email address of the user to invite.",
        json_schema_extra={"example": "user@example.com"},
    )
