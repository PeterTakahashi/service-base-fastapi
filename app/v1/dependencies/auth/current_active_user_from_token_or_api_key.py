from typing import Optional

from fastapi import Depends, Header
from app.models.user import User
from app.v1.dependencies.repositories.user_api_key_repository import (
    get_user_api_key_repository,
)
from app.v1.repositories.user_api_key_repository import UserApiKeyRepository
from app.v1.repositories.user_repository import UserRepository
from app.v1.dependencies.repositories.user_repository import get_user_repository

from app.lib.exception.http.unauthorized import HTTPExceptionUnauthorized
from app.lib.datetime import as_utc, now_utc

from app.lib.fastapi_users.user_setup import optional_current_active_user


async def current_active_user_from_token_or_api_key(
    api_key: Optional[str] = Header(None, alias="X-API-KEY"),
    user_by_token: Optional[User] = Depends(optional_current_active_user),
    user_api_key_repository: UserApiKeyRepository = Depends(
        get_user_api_key_repository
    ),
    user_repository: UserRepository = Depends(get_user_repository),
) -> User:
    """
    1) JWT/Cookie で取得できればそれを返す
    2) できなければ X-API-KEY でユーザーを特定
    3) どちらも無効なら 401
    """
    # ------- 1. token/cookie で認証済み -------
    if user_by_token:
        return user_by_token

    # ------- 2. API キーで認証 -------
    if api_key is None:
        raise HTTPExceptionUnauthorized()

    try:
        user_api_key = await user_api_key_repository.find_by_or_raise(api_key=api_key)
    except Exception:
        raise HTTPExceptionUnauthorized("invalid_api_key")

    # 有効期限チェック
    expires_at_utc = as_utc(user_api_key.expires_at)
    if expires_at_utc and expires_at_utc < now_utc():
        raise HTTPExceptionUnauthorized("expired_api_key")

    user = await user_repository.find(id=user_api_key.user_id)
    return user
