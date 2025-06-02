from app.v1.schemas.wallet_transaction import (
    WalletTransactionRead,
    WalletTransactionSearchParams,
    WalletTransactionListResponse,
)
from app.v1.schemas.common.list.base_list_response import ListResponseMeta


class WalletTransactionService:
    def __init__(self, wallet_transaction_repository):
        self.wallet_transaction_repository = wallet_transaction_repository

    async def get_list(
        self,
        wallet_id: int,
        search_params: WalletTransactionSearchParams,
    ) -> WalletTransactionListResponse:
        """
        Retrieve a list of wallet transactions with filtering, sorting, and pagination.
        """
        wallet_transactions = await self.wallet_transaction_repository.where(
            **search_params.model_dump(exclude_none=True),
            wallet_id=wallet_id,
        )
        total_count = await self.wallet_transaction_repository.count(
            **search_params.model_dump(
                exclude_none=True,
                exclude={"limit", "offset", "sorted_by", "sorted_order"},
            ),
            wallet_id=wallet_id,
        )
        return WalletTransactionListResponse(
            meta=ListResponseMeta(
                total_count=total_count,
                **search_params.model_dump(exclude_none=True),
            ),
            data=[
                WalletTransactionRead.model_validate(tx) for tx in wallet_transactions
            ],
        )

    async def get(
        self, wallet_id: int, wallet_transaction_id: int
    ) -> WalletTransactionRead:
        """
        Retrieve a wallet transaction by its ID.
        """
        wallet_transaction = await self.wallet_transaction_repository.find_by_or_raise(
            wallet_id=wallet_id, id=wallet_transaction_id
        )
        return WalletTransactionRead.model_validate(wallet_transaction)
