from app.v1.schemas.wallet_transaction import WalletTransactionRead
from uuid import UUID


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
