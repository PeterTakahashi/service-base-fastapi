from fastapi import Depends, Header, Request

from app.models.user import User
from app.v1.dependencies.repositories.user_api_key_repository import (
    get_user_api_key_repository,
)
from app.v1.repositories.user_api_key_repository import UserApiKeyRepository
from app.v1.repositories.user_repository import UserRepository
from app.v1.dependencies.repositories.user_repository import get_user_repository


from .authenticate_by_api_key import _authenticate_by_api_key


async def get_user_by_api_key(
    request: Request,
    api_key_str: str = Header(..., alias="X-API-KEY"),
    api_key_repository: UserApiKeyRepository = Depends(get_user_api_key_repository),
    user_repository: UserRepository = Depends(get_user_repository),
) -> User | None:
    api_key = await _authenticate_by_api_key(
        request=request,
        api_key_str=api_key_str,
        api_key_repository=api_key_repository,
        prefix="user_",
    )
    if api_key is None:
        return None

    user = await user_repository.find(id=api_key.user_id)
    return user
