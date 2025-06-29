from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.v1.repositories.user_wallet_repository import UserWalletRepository
from app.db.session import get_async_session
from app.lib.fastapi_users.user_setup import current_active_user


async def get_user_wallet_by_current_active_user(
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    user_wallet_repository = UserWalletRepository(session)
    return await user_wallet_repository.find_by_or_raise(user_id=user.id)
