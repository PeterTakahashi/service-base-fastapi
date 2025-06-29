from app.v1.services.user_api_key_service import UserApiKeyService
from fastapi import Depends
from app.v1.dependencies.repositories.user_api_key_repository import (
    get_user_api_key_repository,
)
from app.v1.repositories.user_api_key_repository import UserApiKeyRepository


def get_user_api_key_service(
    repository: UserApiKeyRepository = Depends(get_user_api_key_repository),
) -> UserApiKeyService:
    return UserApiKeyService(repository)
