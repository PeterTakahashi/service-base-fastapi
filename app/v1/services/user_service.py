from fastapi import Depends, HTTPException, Request, status
from fastapi_users import exceptions, models
from fastapi_users.manager import BaseUserManager
from app.lib.error_code import ErrorCode

from app.v1.repositories.user_repository import UserRepository
from app.models.user import User
from app.v1.schemas.user import UserUpdate, UserRead, UserWithWalletRead
from app.lib.fastapi_users.user_setup import current_active_user
from app.v1.exception_handlers.unprocessable_entity_exception_handler import (
    unprocessable_entity_json_content_with_code,
)


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def get_me(self, user: User) -> UserWithWalletRead:
        user_with_wallet = await self.user_repository.find(
            id=user.id, joinedload_models=[User.wallet]
        )
        return UserWithWalletRead.model_validate(user_with_wallet)

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
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=unprocessable_entity_json_content_with_code(
                    code=ErrorCode.UPDATE_USER_INVALID_PASSWORD,
                    instance=str(request.url),
                    detail=e.reason,
                    source_parameter="password",
                ),
            )
        except exceptions.UserAlreadyExists:
            raise HTTPException(
                status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=ErrorCode.UPDATE_USER_EMAIL_ALREADY_EXISTS,
            )
