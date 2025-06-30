from app.v1.schemas.user_wallet_transaction import (
    UserWalletTransactionRead,
    UserWalletTransactionSearchParams,
    UserWalletTransactionListRead,
)
from app.v1.schemas.common.list.base_list_response import ListResponseMeta


class UserWalletTransactionService:
    def __init__(self, user_wallet_transaction_repository):
        self.user_wallet_transaction_repository = user_wallet_transaction_repository

    async def get_list(
        self,
        user_wallet_id: int,
        search_params: UserWalletTransactionSearchParams,
    ) -> UserWalletTransactionListRead:
        """
        Retrieve a list of user_wallet transactions with filtering, sorting, and pagination.
        """
        user_wallet_transactions = await self.user_wallet_transaction_repository.where(
            **search_params.model_dump(exclude_none=True),
            user_wallet_id=user_wallet_id,
        )
        total_count = await self.user_wallet_transaction_repository.count(
            **search_params.model_dump(
                exclude_none=True,
                exclude={"limit", "offset", "sorted_by", "sorted_order"},
            ),
            user_wallet_id=user_wallet_id,
        )
        return UserWalletTransactionListRead(
            meta=ListResponseMeta(
                total_count=total_count,
                **search_params.model_dump(exclude_none=True),
            ),
            data=[
                UserWalletTransactionRead.model_validate(tx)
                for tx in user_wallet_transactions
            ],
        )

    async def get(
        self, user_wallet_id: int, user_wallet_transaction_id: int
    ) -> UserWalletTransactionRead:
        """
        Retrieve a user_wallet transaction by its ID.
        """
        user_wallet_transaction = (
            await self.user_wallet_transaction_repository.find_by_or_raise(
                user_wallet_id=user_wallet_id, id=user_wallet_transaction_id
            )
        )
        return UserWalletTransactionRead.model_validate(user_wallet_transaction)
