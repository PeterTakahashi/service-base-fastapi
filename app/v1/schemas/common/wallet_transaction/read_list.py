from typing import List
from app.v1.schemas.common.list.base_list_response import BaseListResponse
from app.v1.schemas.common.wallet_transaction.read import WalletTransactionRead


class WalletTransactionListRead(BaseListResponse):
    data: List[WalletTransactionRead]
