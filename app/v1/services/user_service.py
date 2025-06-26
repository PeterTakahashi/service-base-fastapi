from fastapi import Depends, Request, status
from fastapi_users import exceptions, models
from fastapi_users.manager import BaseUserManager
from app.lib.error_code import ErrorCode

from app.v1.repositories.user_repository import UserRepository
from app.v1.repositories.user_address_repository import UserAddressRepository
from app.models.user import User
from app.v1.schemas.user import UserUpdate, UserWithRelationRead
from app.lib.fastapi_users.user_setup import current_active_user
from app.lib.exception.api_exception import init_api_exception


class UserService:
    def __init__(
        self,
        user_repository: UserRepository,
        user_address_repository: UserAddressRepository,
    ):
        self.user_repository = user_repository
        self.user_address_repository = user_address_repository

    async def get_me(self, user: User) -> UserWithRelationRead:
        user_with_user_wallet = await self.user_repository.find(
            id=user.id, joinedload_models=[User.user_wallet, User.address]
        )
        return UserWithRelationRead.model_validate(user_with_user_wallet)

    async def update_me(
        self,
        request: Request,
        user_manager: BaseUserManager[models.UP, models.ID],
        user_update: UserUpdate,
        user: User = Depends(current_active_user),
    ) -> UserWithRelationRead:
        try:
            user = await user_manager.update(
                user_update, user, safe=True, request=request  # type: ignore
            )
            if user_update.address:
                address = await self.user_address_repository.find_by(user_id=user.id)
                if address:
                    await self.user_address_repository.update(
                        id=address.id, **user_update.address.model_dump()
                    )
                else:
                    await self.user_address_repository.create(
                        **user_update.address.model_dump(), user_id=user.id
                    )
            user = await self.user_repository.find(
                id=user.id, joinedload_models=[User.user_wallet, User.address]
            )
            return UserWithRelationRead.model_validate(user)
        except exceptions.InvalidPasswordException as e:
            raise init_api_exception(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail_code=ErrorCode.UPDATE_USER_INVALID_PASSWORD,
                detail_detail=e.reason,
                pointer="password",
            )
        except exceptions.UserAlreadyExists:
            raise init_api_exception(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail_code=ErrorCode.UPDATE_USER_EMAIL_ALREADY_EXISTS,
                pointer="email",
            )
