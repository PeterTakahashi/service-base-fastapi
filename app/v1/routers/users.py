from fastapi import APIRouter, Depends, Request, status
from fastapi_users import models
from fastapi_users.manager import BaseUserManager
from fastapi_users.router.common import ErrorCode, ErrorModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.lib.fastapi_users.user_setup import current_active_user
from app.v1.schemas.user import UserRead, UserUpdate
from app.models.user import User
from app.db.session import get_async_session
from app.v1.repositories.user_repository import UserRepository
from app.v1.services.user_service import UserService
from app.lib.fastapi_users.user_manager import get_user_manager

router = APIRouter()


def get_user_service(session: AsyncSession = Depends(get_async_session)) -> UserService:
    repo = UserRepository(session)
    return UserService(repo)


@router.get("/me", response_model=UserRead, name="users:get_current_user")
async def get_me(
    user: User = Depends(current_active_user),
    service: UserService = Depends(get_user_service),
):
    return await service.get_me(user)


@router.patch(
    "/me",
    response_model=UserRead,
    name="users:patch_current_user",
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorModel,
            "content": {
                "application/json": {
                    "examples": {
                        ErrorCode.UPDATE_USER_EMAIL_ALREADY_EXISTS: {
                            "summary": "A user with this email already exists.",
                            "value": {
                                "detail": ErrorCode.UPDATE_USER_EMAIL_ALREADY_EXISTS
                            },
                        },
                        ErrorCode.UPDATE_USER_INVALID_PASSWORD: {
                            "summary": "Password validation failed.",
                            "value": {
                                "detail": {
                                    "code": ErrorCode.UPDATE_USER_INVALID_PASSWORD,
                                    "reason": "Password should be"
                                    "at least 3 characters",
                                }
                            },
                        },
                    }
                }
            },
        },
    },
)
async def update_me(
    request: Request,
    user_update: UserUpdate,  # type: ignore
    user: User = Depends(current_active_user),
    user_manager: BaseUserManager[models.UP, models.ID] = Depends(get_user_manager),
    service: UserService = Depends(get_user_service),
):
    return await service.update_me(
        request=request,
        user_manager=user_manager,
        user_update=user_update,
        user=user,
    )
