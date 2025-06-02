from app.db.session import get_async_session
from app.v1.repositories.user_api_key_repository import UserApiKeyRepository
from app.v1.services.user_api_key_service import UserApiKeyService
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends


def get_user_api_key_service(
    session: AsyncSession = Depends(get_async_session),
) -> UserApiKeyService:
    repo = UserApiKeyRepository(session)
    return UserApiKeyService(repo)
