from datetime import datetime
from pydantic import Field, ConfigDict
from app.models.enums.wallet_transaction import (
    WalletTransactionType,
    WalletTransactionStatus,
)
from app.v1.schemas.common.id_encoder import HasEncodedID
from app.v1.schemas.balance import Balance


class UserWalletTransactionRead(HasEncodedID):
    """
    Schema for reading user_wallet transaction information.
    """

    amount: Balance = Field(
        ...,
        description="The amount of the transaction in USD",
        json_schema_extra={"example": "10.00"},
    )
    balance_after_transaction: Balance | None = Field(
        None,
        description="The balance after the transaction in USD",
        json_schema_extra={"example": "100.00"},
    )
    user_wallet_transaction_type: WalletTransactionType = Field(
        ...,
        description="The type of the user_wallet transaction (e.g., 'deposit', 'spend').",
        json_schema_extra={"example": WalletTransactionType.DEPOSIT.value},
    )
    user_wallet_transaction_status: WalletTransactionStatus = Field(
        ...,
        description="The status of the user_wallet transaction (e.g., 'pending', 'completed').",
        json_schema_extra={"example": WalletTransactionStatus.COMPLETED.value},
    )
    created_at: datetime = Field(
        ...,
        description="The date and time when the transaction was created.",
        json_schema_extra={"example": "2023-10-01T12:00:00Z"},
    )
    updated_at: datetime = Field(
        ...,
        description="The date and time when the transaction was last updated.",
        json_schema_extra={"example": "2023-10-01T12:00:00Z"},
    )
    model_config = ConfigDict(from_attributes=True)
