from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class UserApiKeyCreate(BaseModel):
    name: str = Field(
        ...,
        description="Name of the API key",
        json_schema_extra={"example": "My API Key"},
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


class UserApiKeyUpdate(BaseModel):
    name: Optional[str] = Field(
        None,
        description="Updated name of the API key",
        json_schema_extra={"example": "My Updated API Key"},
    )
    expires_at: Optional[datetime] = Field(
        None,
        description="Updated expiration datetime",
        json_schema_extra={"example": "2025-12-31T23:59:59Z"},
    )
    allowed_origin: Optional[str] = Field(
        None,
        description="Updated CORS allowed origin",
        json_schema_extra={"example": "https://example.com"},
    )
    allowed_ip: Optional[str] = Field(
        None,
        description="Updated allowed IP address",
        json_schema_extra={"example": "192.168.1.1"},
    )

    model_config = ConfigDict(from_attributes=True)
