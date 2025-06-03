from datetime import datetime, timezone
from typing import Optional

from fastapi import Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_async_session
from app.lib.fastapi_users.user_setup import fastapi_users
from app.models.user import User
from app.v1.repositories.user_api_key_repository import UserApiKeyRepository
from app.v1.repositories.user_repository import UserRepository

from app.lib.exception.http.unauthorized import HTTPExceptionUnauthorized

# fastapi-users には optional=True がある
optional_current_active_user = fastapi_users.current_user(
    active=True, verified=True, optional=True
)


async def current_active_user_from_token_or_api_key(
    api_key: Optional[str] = Header(None, alias="X-API-KEY"),
    user_by_token: Optional[User] = Depends(optional_current_active_user),
    session: AsyncSession = Depends(get_async_session),
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
        raise HTTPExceptionUnauthorized("missing_api_key")

    repo = UserApiKeyRepository(session)
    try:
        user_api_key = await repo.find_by_or_raise(api_key=api_key)
    except Exception:
        raise HTTPExceptionUnauthorized("invalid_api_key")

    # 有効期限チェック
    if user_api_key.expires_at and user_api_key.expires_at < datetime.now(
        tz=timezone.utc
    ):
        raise HTTPExceptionUnauthorized("expired_api_key")

    user = await UserRepository(session).find(id=user_api_key.user_id)
    return user
