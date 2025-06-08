from typing import Optional, List
from fastapi import Query
from app.models.wallet_transaction import WalletTransactionType, WalletTransactionStatus
from datetime import datetime
from app.v1.schemas.wallet_transaction.search_params import (
    WalletTransactionSearchParams,
)


def get_wallet_transaction_search_params(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    sorted_by: str = Query("created_at"),
    sorted_order: str = Query("desc"),
    amount__gte: Optional[int] = Query(None),
    amount__lte: Optional[int] = Query(None),
    wallet_transaction_type__in: Optional[List[WalletTransactionType]] = Query(None),
    wallet_transaction_status__in: Optional[List[WalletTransactionStatus]] = Query(
        None
    ),
    created_at__gte: Optional[datetime] = Query(None),
    created_at__lte: Optional[datetime] = Query(None),
    updated_at__gte: Optional[datetime] = Query(None),
    updated_at__lte: Optional[datetime] = Query(None),
) -> WalletTransactionSearchParams:
    return WalletTransactionSearchParams(
        limit=limit,
        offset=offset,
        sorted_by=sorted_by,
        sorted_order=sorted_order,
        amount__gte=amount__gte,
        amount__lte=amount__lte,
        wallet_transaction_type__in=wallet_transaction_type__in,
        wallet_transaction_status__in=wallet_transaction_status__in,
        created_at__gte=created_at__gte,
        created_at__lte=created_at__lte,
        updated_at__gte=updated_at__gte,
        updated_at__lte=updated_at__lte,
    )
