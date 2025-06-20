from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class UserWalletRead(BaseModel):
    """
    Schema for reading user_wallet information.
    """

    balance: int = Field(
        ...,
        description="The current balance of the user_wallet.",
        json_schema_extra={"example": 1000},  # Example: $10.00 in cents,
    )
    created_at: datetime = Field(
        ...,
        description="The date and time when the user_wallet was created.",
        json_schema_extra={"example": "2023-10-01T12:00:00Z"},
    )
    updated_at: datetime = Field(
        ...,
        description="The date and time when the user_wallet was last updated.",
        json_schema_extra={"example": "2023-10-01T12:00:00Z"},
    )
    model_config = ConfigDict(from_attributes=True)
