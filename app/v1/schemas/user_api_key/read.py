from datetime import datetime
from pydantic import Field
from app.v1.schemas.common.id_encoder import HasEncodedID


class UserApiKeyRead(HasEncodedID):
    name: str = Field(..., description="Name of the API key", example="My API Key")
    api_key: str = Field(
        ..., description="The actual API key", example="sk_test_1234567890abcdef"
    )
    expires_at: datetime | None = Field(
        None, description="Expiration datetime of the API key"
    )
    allowed_origin: str | None = Field(None, description="CORS allowed origin")
    allowed_ip: str | None = Field(None, description="Allowed IP address")
    created_at: datetime = Field(..., description="Creation datetime of the API key")
    updated_at: datetime = Field(
        ..., description="Last updated datetime of the API key"
    )
