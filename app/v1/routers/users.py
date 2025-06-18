from fastapi import APIRouter, Depends, Request, status
from fastapi_users import models
from fastapi_users.manager import BaseUserManager
from app.lib.error_code import ErrorCode

from app.lib.fastapi_users.user_setup import current_active_user
from app.v1.schemas.user import UserRead, UserUpdate, UserWithWalletRead
from app.models.user import User
from app.v1.services.user_service import UserService
from app.lib.fastapi_users.user_manager import get_user_manager
from app.v1.dependencies.services.user_service import get_user_service


from app.lib.utils.openapi_response_type import openapi_response_type
from app.schemas.api_exception_openapi_example import APIExceptionOpenAPIExample

router = APIRouter(prefix="/users", tags=["Users"])


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
        status.HTTP_422_UNPROCESSABLE_ENTITY: openapi_response_type(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            request_path="/app/v1/users/me",
            api_exception_openapi_examples=[
                APIExceptionOpenAPIExample(
                    detail_code=ErrorCode.UPDATE_USER_EMAIL_ALREADY_EXISTS,
                    pointer="email",
                ),
                APIExceptionOpenAPIExample(
                    detail_code=ErrorCode.UPDATE_USER_INVALID_PASSWORD,
                    pointer="password",
                ),
            ],
        ),
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
