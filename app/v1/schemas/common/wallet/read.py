from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from app.v1.schemas.balance import Balance


class WalletRead(BaseModel):
    """
    Schema for reading user_wallet information.
    """

    balance: Balance = Field(
        ...,
        description="The current balance of the user_wallet.",
        json_schema_extra={"example": "10.00"},
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
