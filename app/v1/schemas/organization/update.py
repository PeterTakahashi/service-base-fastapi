from pydantic import Field, EmailStr
from typing import Optional
from .create import OrganizationCreate


class OrganizationUpdate(OrganizationCreate):
    name: Optional[str] = Field(default=None, max_length=255)
    profile_image_key: Optional[str] = Field(default=None)
    billing_email: Optional[EmailStr] = Field(default=None)
