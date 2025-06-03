from pydantic import BaseModel
from pydantic import Field, ConfigDict


class UserApiKeyVerifyResponse(BaseModel):
    """
    Response model for verifying an API key.
    """

    is_valid: bool = Field(
        ...,
        description="Indicates whether the API key is valid",
        json_schema_extra={"example": True},
    )
    model_config = ConfigDict(from_attributes=True)
