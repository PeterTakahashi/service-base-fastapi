from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_async_session

from app.v1.repositories.user_wallet_transaction_repository import (
    UserWalletTransactionRepository,
)
from app.v1.services.user_wallet_transaction_service import UserWalletTransactionService


def get_user_wallet_transaction_service(
    session: AsyncSession = Depends(get_async_session),
) -> UserWalletTransactionService:
    user_wallet_transaction_repository = UserWalletTransactionRepository(session)
    return UserWalletTransactionService(user_wallet_transaction_repository)
