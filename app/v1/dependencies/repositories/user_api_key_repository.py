from app.v1.repositories.user_api_key_repository import UserApiKeyRepository
from app.db.session import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends


def get_user_api_key_repository(
    session: AsyncSession = Depends(get_async_session),
) -> UserApiKeyRepository:
    return UserApiKeyRepository(session)
