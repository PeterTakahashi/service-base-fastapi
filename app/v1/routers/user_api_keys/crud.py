from fastapi import APIRouter, Depends, Request, status

from app.v1.schemas.user_api_key import (
    UserApiKeyListRead,
    UserApiKeyRead,
    UserApiKeyCreate,
    UserApiKeyUpdate,
    UserApiKeySearchParams,
)
from app.v1.dependencies.services.user_api_key_service import get_user_api_key_service
from app.v1.dependencies.models.user_api_key.get_user_api_key import get_user_api_key
from app.v1.services.user_api_key_service import UserApiKeyService
from app.lib.fastapi_users.user_setup import current_active_user
from app.models.user import User
from app.models.user_api_key import UserApiKey

router = APIRouter()


@router.get(
    "",
    response_model=UserApiKeyListRead,
    name="user_api_keys:list_user_api_keys",
)
async def list_user_api_keys(
    request: Request,
    search_params: UserApiKeySearchParams = Depends(),
    user: User = Depends(current_active_user),
    service: UserApiKeyService = Depends(get_user_api_key_service),
):
    """
    Retrieve a list of user API keys with filtering, sorting, and pagination.
    """
    return await service.get_list(user_id=user.id, search_params=search_params)


@router.get(
    "/{user_api_key_id}",
    response_model=UserApiKeyRead,
    name="user_api_keys:get_user_api_keys",
)
async def get_user_api_keys(
    user_api_key: UserApiKey = Depends(get_user_api_key),
):
    """
    Retrieve a user API key by its ID.
    """
    return UserApiKeyRead.model_validate(user_api_key)


@router.post(
    "",
    response_model=UserApiKeyRead,
    status_code=status.HTTP_201_CREATED,
    name="user_api_keys:create_user_api_key",
)
async def create_user_api_key(
    request: Request,
    user_api_key_create: UserApiKeyCreate,
    user: User = Depends(current_active_user),
    service: UserApiKeyService = Depends(get_user_api_key_service),
):
    """
    Create a new user API key.
    """
    return await service.create(
        user_id=user.id, user_api_key_create=user_api_key_create
    )


@router.patch(
    "/{user_api_key_id}",
    response_model=UserApiKeyRead,
    name="user_api_keys:update_user_api_key",
)
async def update_user_api_key(
    request: Request,
    user_api_key_update: UserApiKeyUpdate,
    user_api_key: UserApiKey = Depends(get_user_api_key),
    service: UserApiKeyService = Depends(get_user_api_key_service),
):
    """
    Update an existing user API key.
    """
    return await service.update(
        user_api_key_id=user_api_key.id, user_api_key_update=user_api_key_update
    )


@router.delete(
    "/{user_api_key_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    name="user_api_keys:delete_user_api_key",
)
async def delete_user_api_key(
    request: Request,
    user_api_key: UserApiKey = Depends(get_user_api_key),
    service: UserApiKeyService = Depends(get_user_api_key_service),
) -> None:
    """
    Delete a user API key.
    """
    await service.delete(user_api_key_id=user_api_key.id)
    return None
