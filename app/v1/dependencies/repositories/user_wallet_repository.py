from app.v1.repositories.user_wallet_repository import UserWalletRepository
from app.db.session import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends


def get_user_wallet_repository(
    session: AsyncSession = Depends(get_async_session),
) -> UserWalletRepository:
    return UserWalletRepository(session)
