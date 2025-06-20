from datetime import datetime
from pydantic import Field
from app.models.user_wallet_transaction import (
    UserWalletTransactionType,
    UserWalletTransactionStatus,
)
from app.v1.schemas.common.id_encoder import HasEncodedID


class UserWalletTransactionRead(HasEncodedID):
    """
    Schema for reading user_wallet transaction information.
    """

    amount: int = Field(
        ...,
        description="The amount of the transaction in cents.",
        json_schema_extra={"example": 1000},
    )
    user_wallet_transaction_type: UserWalletTransactionType = Field(
        ...,
        description="The type of the user_wallet transaction (e.g., 'deposit', 'spend').",
        json_schema_extra={"example": UserWalletTransactionType.DEPOSIT.value},
    )
    user_wallet_transaction_status: UserWalletTransactionStatus = Field(
        ...,
        description="The status of the user_wallet transaction (e.g., 'pending', 'completed').",
        json_schema_extra={"example": UserWalletTransactionStatus.COMPLETED.value},
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
