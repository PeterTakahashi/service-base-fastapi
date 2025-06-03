from fastapi import Depends
from app.models.user import User
from app.v1.dependencies.repositories.user_api_key_repository import (
    get_user_api_key_repository,
)
from app.v1.repositories.user_api_key_repository import UserApiKeyRepository
from app.lib.fastapi_users.user_setup import current_active_user
from app.lib.convert_id import decode_id


async def get_user_api_key(
    user_api_key_id: str,
    user: User = Depends(current_active_user),
    user_api_key_repository: UserApiKeyRepository = Depends(
        get_user_api_key_repository
    ),
):
    return await user_api_key_repository.find_by_or_raise(
        user_id=user.id, id=decode_id(user_api_key_id)
    )
