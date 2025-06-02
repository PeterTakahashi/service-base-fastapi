from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class UserApiKeyCreate(BaseModel):
    name: str = Field(..., description="Name of the API key", example="My API Key")
    expires_at: Optional[datetime] = Field(
        None, description="Expiration datetime of the API key"
    )
    allowed_origin: Optional[str] = Field(None, description="CORS allowed origin")
    allowed_ip: Optional[str] = Field(None, description="Allowed IP address")

    model_config = ConfigDict(from_attributes=True)


class UserApiKeyUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Updated name of the API key")
    expires_at: Optional[datetime] = Field(
        None, description="Updated expiration datetime"
    )
    allowed_origin: Optional[str] = Field(
        None, description="Updated CORS allowed origin"
    )
    allowed_ip: Optional[str] = Field(None, description="Updated allowed IP address")

    model_config = ConfigDict(from_attributes=True)
