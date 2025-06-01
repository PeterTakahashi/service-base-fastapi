from uuid import UUID
from typing import List
from app.v1.schemas.wallet_transaction import (
    WalletTransactionRead,
    WalletTransactionSearchParams,
)


class WalletTransactionService:
    def __init__(self, wallet_repository, wallet_transaction_repository):
        self.wallet_repository = wallet_repository
        self.wallet_transaction_repository = wallet_transaction_repository

    async def get(
        self, user_id: UUID, wallet_transaction_id: int
    ) -> WalletTransactionRead:
        """
        Retrieve a wallet transaction by its ID.
        """
        wallet = await self.wallet_repository.find_by_or_raise(user_id=user_id)
        wallet_transaction = await self.wallet_transaction_repository.find_by_or_raise(
            wallet_id=wallet.id, id=wallet_transaction_id
        )
        return WalletTransactionRead.model_validate(wallet_transaction)

    async def get_list(
        self,
        user_id: UUID,
        search_params: WalletTransactionSearchParams,
    ) -> List[WalletTransactionRead]:
        """
        Retrieve a list of wallet transactions with filtering, sorting, and pagination.
        """
        wallet = await self.wallet_repository.find_by_or_raise(user_id=user_id)
        query_search_params = search_params.model_dump(
            exclude_unset=True, exclude={"limit", "offset", "sorted_by", "sorted_order"}
        )
        query_search_params["wallet_id"] = wallet.id
        cleaned_search_params = {
            k: v for k, v in query_search_params.items() if v is not None
        }
        wallet_transactions = await self.wallet_transaction_repository.where(
            limit=search_params.limit,
            offset=search_params.offset,
            sorted_by=search_params.sorted_by,
            sorted_order=search_params.sorted_order,
            **cleaned_search_params,
        )
        return [WalletTransactionRead.model_validate(tx) for tx in wallet_transactions]
