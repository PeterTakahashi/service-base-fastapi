from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.v1.repositories.wallet_repository import WalletRepository
from app.db.session import get_async_session
from app.lib.fastapi_users.user_setup import current_active_user


async def get_wallet_by_current_active_user(
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    wallet_repository = WalletRepository(session)
    return await wallet_repository.find_by_or_raise(user_id=user.id)
