from datetime import datetime
from pydantic import Field
from app.v1.schemas.common.id_encoder import HasEncodedID


class UserApiKeyRead(HasEncodedID):
    name: str = Field(
        ...,
        description="Name of the API key",
        json_schema_extra={"example": "My API Key"},
        max_length=255,
        min_length=1,
    )
    api_key: str = Field(
        ...,
        description="The actual API key",
        json_schema_extra={"example": "1234567890abcdef"},
    )
    expires_at: datetime | None = Field(
        None,
        description="Expiration datetime of the API key",
        json_schema_extra={"example": "2024-12-31T23:59:59Z"},
    )
    allowed_origin: str | None = Field(
        None,
        description="CORS allowed origin",
        json_schema_extra={"example": "https://example.com"},
    )
    allowed_ip: str | None = Field(
        None,
        description="Allowed IP address",
        json_schema_extra={"example": "192.168.1.1"},
    )
    created_at: datetime = Field(
        ...,
        description="Creation datetime of the API key",
        json_schema_extra={"example": "2023-10-01T12:00:00Z"},
    )
    updated_at: datetime = Field(
        ...,
        description="Last updated datetime of the API key",
        json_schema_extra={"example": "2023-10-01T12:00:00Z"},
    )
