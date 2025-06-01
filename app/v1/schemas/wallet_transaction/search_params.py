from typing import Optional
from datetime import datetime
from app.v1.schemas.base_search_params import BaseSearchParams
from app.models.wallet_transaction import WalletTransactionType, WalletTransactionStatus


class WalletTransactionSearchParams(BaseSearchParams):
    amount__gte: Optional[int] = None
    amount__lte: Optional[int] = None
    created_at__gte: Optional[datetime] = None
    created_at__lte: Optional[datetime] = None
    wallet_transaction_type__exact: Optional[WalletTransactionType] = None
    wallet_transaction_status__exact: Optional[WalletTransactionStatus] = None
