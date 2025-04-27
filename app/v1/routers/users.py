from fastapi import APIRouter, Depends
from app.core.user_setup import current_active_user
from app.v1.schemas.user import UserRead, UserUpdate
from app.v1.models.user import User
from app.core.response_type import unauthorized_response
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_async_session
from app.v1.repositories.user_repository import UserRepository
from app.v1.services.user_service import UserService

router = APIRouter()


def get_user_service(session: AsyncSession = Depends(get_async_session)) -> UserService:
    repo = UserRepository(session)
    return UserService(repo)


@router.get("/me", response_model=UserRead, responses=unauthorized_response)
async def get_me(
    user: User = Depends(current_active_user),
    service: UserService = Depends(get_user_service),
):
    return await service.get_me(user)


@router.patch("/me", response_model=UserRead, responses=unauthorized_response)
async def update_me(
    data: UserUpdate,
    user: User = Depends(current_active_user),
    service: UserService = Depends(get_user_service),
):
    return await service.update_me(user, data)
