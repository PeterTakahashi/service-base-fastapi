from typing import List
from app.v1.schemas.base_list_response import BaseListResponse
from app.v1.schemas.wallet_transaction.read import WalletTransactionRead


class WalletTransactionListResponse(BaseListResponse):
    data: List[WalletTransactionRead]
