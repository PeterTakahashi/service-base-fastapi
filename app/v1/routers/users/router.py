from fastapi import APIRouter, Depends, Request
from fastapi_users import models
from fastapi_users.manager import BaseUserManager

from app.lib.fastapi_users.user_setup import current_active_user
from app.v1.schemas.user import UserUpdate, UserWithRelationRead
from app.models.user import User
from app.v1.services.user_service import UserService
from app.lib.fastapi_users.user_manager import get_user_manager
from app.v1.dependencies.services.user_service import get_user_service


from app.v1.routers.users.response_type import UPDATE_USER_RESPONSES

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserWithRelationRead, name="users:get_current_user")
async def get_me(
    user: User = Depends(current_active_user),
    service: UserService = Depends(get_user_service),
):
    return await service.get_me(user)


@router.patch(
    "/me",
    response_model=UserWithRelationRead,
    name="users:patch_current_user",
    responses=UPDATE_USER_RESPONSES,  # type: ignore
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
