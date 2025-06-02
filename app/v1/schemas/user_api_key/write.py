from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, field_validator


class UserApiKeyCreate(BaseModel):
    name: str = Field(
        ...,
        description="Name of the API key",
        json_schema_extra={"example": "My API Key"},
        max_length=255,
        min_length=1,
    )
    expires_at: Optional[datetime] = Field(
        None,
        description="Expiration datetime of the API key",
        json_schema_extra={"example": "2024-12-31T23:59:59Z"},
    )
    allowed_origin: Optional[str] = Field(
        None,
        description="CORS allowed origin",
        json_schema_extra={"example": "https://example.com"},
    )
    allowed_ip: Optional[str] = Field(
        None,
        description="Allowed IP address",
        json_schema_extra={"example": "192.168.1.1"},
    )

    model_config = ConfigDict(from_attributes=True)

    @field_validator("expires_at")
    def validate_expires_at(cls, value: Optional[datetime]) -> Optional[datetime]:
        if value and value < datetime.utcnow():
            raise ValueError("The expiration datetime cannot be in the past.")
        return value


class UserApiKeyUpdate(UserApiKeyCreate):
    pass
