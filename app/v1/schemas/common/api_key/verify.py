from pydantic import BaseModel
from pydantic import Field, ConfigDict
from typing import Literal


class ApiKeyVerifyResponse(BaseModel):
    """
    Response model for verifying an API key.
    """

    is_valid: bool = Field(
        ...,
        description="Indicates whether the API key is valid",
        json_schema_extra={"example": True},
    )
    owner_type: Literal["user", "organization"] = Field(
        ...,
        description="Type of the owner (user or organization)",
        json_schema_extra={"example": "user"},
    )
    model_config = ConfigDict(from_attributes=True)
