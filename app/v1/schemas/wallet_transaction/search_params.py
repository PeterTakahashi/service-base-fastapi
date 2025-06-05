from typing import Optional, List
from datetime import datetime
from app.v1.schemas.common.list.base_search_params import BaseSearchParams
from app.models.wallet_transaction import WalletTransactionType, WalletTransactionStatus


class WalletTransactionSearchParams(BaseSearchParams):
    amount__gte: Optional[int] = None
    amount__lte: Optional[int] = None
    created_at__gte: Optional[datetime] = None
    created_at__lte: Optional[datetime] = None
    updated_at__gte: Optional[datetime] = None
    updated_at__lte: Optional[datetime] = None
    wallet_transaction_type__in: Optional[List[WalletTransactionType]] = None
    wallet_transaction_status__in: Optional[List[WalletTransactionStatus]] = None
