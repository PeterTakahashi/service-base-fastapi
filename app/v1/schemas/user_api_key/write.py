from datetime import datetime, timezone
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

    @field_validator("expires_at", mode="before")
    def parse_epoch_or_iso(cls, v):
        if isinstance(v, (int, float)):
            v = datetime.fromtimestamp(v, tz=timezone.utc)
        if isinstance(v, str) and v.endswith("Z"):
            v = v.replace("Z", "+00:00")

        if isinstance(v, datetime) and v.tzinfo is None:
            v = v.replace(tzinfo=timezone.utc)
        return v

    @field_validator("expires_at")
    def validate_expires_at(cls, value: Optional[datetime]) -> Optional[datetime]:
        if value and value < datetime.now(timezone.utc):
            raise ValueError("The expiration datetime cannot be in the past.")
        return value


class UserApiKeyUpdate(UserApiKeyCreate):
    pass
