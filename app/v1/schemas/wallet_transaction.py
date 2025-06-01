from pydantic import Field, ConfigDict
from typing import Optional
from datetime import datetime
from app.models.wallet_transaction import WalletTransactionType, WalletTransactionStatus
from app.v1.schemas.base import HasEncodedID
from app.v1.schemas.base_search_params import BaseSearchParams


class WalletTransactionSearchParams(BaseSearchParams):
    amount__gte: Optional[int] = None
    amount__lte: Optional[int] = None
    created_at__gte: Optional[datetime] = None
    created_at__lte: Optional[datetime] = None
    wallet_transaction_type__exact: Optional[WalletTransactionType] = None
    wallet_transaction_status__exact: Optional[WalletTransactionStatus] = None


class WalletTransactionRead(HasEncodedID):
    """
    Schema for reading wallet transaction information.
    """

    amount: int = Field(
        ...,
        description="The amount of the transaction in cents.",
        json_schema_extra={"example": 1000},
    )
    wallet_transaction_type: WalletTransactionType = Field(
        ...,
        description="The type of the wallet transaction (e.g., 'deposit', 'withdrawal').",
        json_schema_extra={"example": WalletTransactionType.DEPOSIT.value},
    )
    wallet_transaction_status: WalletTransactionStatus = Field(
        ...,
        description="The status of the wallet transaction (e.g., 'pending', 'completed').",
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
