from app.v1.repositories.user_repository import UserRepository
from app.v1.services.user_service import UserService
from fastapi import Depends
from app.v1.dependencies.repositories.user_repository import get_user_repository
from app.v1.repositories.user_address_repository import UserAddressRepository
from app.v1.dependencies.repositories.user_address_repository import (
    get_user_address_repository,
)


def get_user_service(
    user_repository: UserRepository = Depends(get_user_repository),
    user_address_repository: UserAddressRepository = Depends(
        get_user_address_repository
    ),
) -> UserService:
    return UserService(
        user_repository=user_repository, user_address_repository=user_address_repository
    )
