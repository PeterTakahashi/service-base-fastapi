from app.v1.repositories.user_wallet_transaction_repository import UserWalletTransactionRepository
from app.db.session import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends


def get_user_wallet_transaction_repository(
    session: AsyncSession = Depends(get_async_session),
) -> UserWalletTransactionRepository:
    return UserWalletTransactionRepository(session)
