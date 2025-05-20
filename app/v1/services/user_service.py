from fastapi import Depends, HTTPException, Request, status
from fastapi_users import exceptions, models
from fastapi_users.manager import BaseUserManager
from fastapi_users.router.common import ErrorCode

from app.v1.repositories.user_repository import UserRepository
from app.models.user import User
from app.v1.schemas.user import UserUpdate, UserRead
from app.lib.fastapi_users.user_setup import current_active_user


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def get_me(self, user: User) -> UserRead:
        return UserRead.model_validate(user)

    async def update_me(
        self,
        request: Request,
        user_manager: BaseUserManager[models.UP, models.ID],
        user_update: UserUpdate,
        user: User = Depends(current_active_user),
    ) -> UserRead:
        try:
            user = await user_manager.update(
                user_update, user, safe=True, request=request  # type: ignore
            )
            return UserRead.model_validate(user)
        except exceptions.InvalidPasswordException as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "code": ErrorCode.UPDATE_USER_INVALID_PASSWORD,
                    "reason": e.reason,
                },
            )
        except exceptions.UserAlreadyExists:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                detail=ErrorCode.UPDATE_USER_EMAIL_ALREADY_EXISTS,
            )
