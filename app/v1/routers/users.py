from fastapi import APIRouter, Depends, Request, status
from fastapi_users import models
from fastapi_users.manager import BaseUserManager
from app.lib.error_code import ErrorCode
from app.lib.schemas.error import ErrorResponse

from app.lib.fastapi_users.user_setup import current_active_user
from app.v1.schemas.user import UserRead, UserUpdate, UserWithWalletRead
from app.models.user import User
from app.v1.services.user_service import UserService
from app.lib.fastapi_users.user_manager import get_user_manager
from app.v1.dependencies.services.user_service import get_user_service

from app.v1.exception_handlers.unprocessable_entity_exception_handler import (
    unprocessable_entity_json_content_with_code,
)

router = APIRouter()


@router.get("/me", response_model=UserWithWalletRead, name="users:get_current_user")
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
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": ErrorResponse,
            "content": {
                "application/json": {
                    "examples": {
                        ErrorCode.UPDATE_USER_EMAIL_ALREADY_EXISTS: {
                            "summary": "A user with this email already exists.",
                            "value": unprocessable_entity_json_content_with_code(
                                code=ErrorCode.UPDATE_USER_EMAIL_ALREADY_EXISTS,
                                instance="http://127.0.0.1:8000/app/v1/auth/register/register",
                                source_parameter="email",
                            ),
                        },
                        ErrorCode.UPDATE_USER_INVALID_PASSWORD: {
                            "summary": "Password validation failed.",
                            "value": unprocessable_entity_json_content_with_code(
                                code=ErrorCode.UPDATE_USER_INVALID_PASSWORD,
                                instance="http://127.0.0.1:8000/app/v1/auth/register/register",
                                detail="Password must be at least 8 characters long",
                                source_parameter="password",
                            ),
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
