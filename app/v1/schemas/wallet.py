from pydantic import BaseModel, Field


class WalletRead(BaseModel):
    """
    Schema for reading wallet information.
    """
    balance: int = Field(
        ...,
        description="The current balance of the wallet.",
        json_schema_extra={"example": 1000}  # Example: $10.00 in cents,
    )
    created_at: str = Field(
        ...,
        description="The date and time when the wallet was created.",
        json_schema_extra={"example": "2023-10-01T12:00:00Z"},
    )
    updated_at: str = Field(
        ...,
        description="The date and time when the wallet was last updated.",
        json_schema_extra={"example": "2023-10-01T12:00:00Z"},
    )
