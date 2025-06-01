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
        self, wallet_id: int, wallet_transaction_id: int
    ) -> WalletTransactionRead:
        """
        Retrieve a wallet transaction by its ID.
        """
        wallet_transaction = await self.wallet_transaction_repository.find_by_or_raise(
            wallet_id=wallet_id, id=wallet_transaction_id
        )
        return WalletTransactionRead.model_validate(wallet_transaction)

    async def get_list(
        self,
        wallet_id: int,
        search_params: WalletTransactionSearchParams,
    ) -> List[WalletTransactionRead]:
        """
        Retrieve a list of wallet transactions with filtering, sorting, and pagination.
        """
        wallet_transactions = await self.wallet_transaction_repository.where(
            **search_params.model_dump(exclude_none=True),
            wallet_id=wallet_id,
        )
        return [WalletTransactionRead.model_validate(tx) for tx in wallet_transactions]
