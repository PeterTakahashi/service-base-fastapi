from fastapi import Depends
from app.models.user import User
from app.v1.repositories.user_wallet_repository import UserWalletRepository
from app.lib.fastapi_users.user_setup import current_active_user
from app.v1.dependencies.repositories.user_wallet_repository import (
    get_user_wallet_repository,
)


async def get_user_wallet_by_current_active_user(
    user: User = Depends(current_active_user),
    user_wallet_repository: UserWalletRepository = Depends(get_user_wallet_repository),
):
    return await user_wallet_repository.find_by_or_raise(user_id=user.id)
