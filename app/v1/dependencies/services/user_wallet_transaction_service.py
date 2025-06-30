from fastapi import Depends

from app.v1.repositories.user_wallet_transaction_repository import (
    UserWalletTransactionRepository,
)
from app.v1.services.user_wallet_transaction_service import UserWalletTransactionService
from app.v1.dependencies.repositories.user_wallet_transaction_repository import (
    get_user_wallet_transaction_repository,
)


def get_user_wallet_transaction_service(
    user_wallet_transaction_repository: UserWalletTransactionRepository = Depends(
        get_user_wallet_transaction_repository
    ),
) -> UserWalletTransactionService:
    return UserWalletTransactionService(user_wallet_transaction_repository)
