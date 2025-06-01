from app.db.session import get_async_session
from app.v1.repositories.user_repository import UserRepository
from app.v1.services.user_service import UserService
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends


def get_user_service(session: AsyncSession = Depends(get_async_session)) -> UserService:
    repo = UserRepository(session)
    return UserService(repo)
