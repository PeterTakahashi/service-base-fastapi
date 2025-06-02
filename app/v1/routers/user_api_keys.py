from fastapi import APIRouter, Depends, Request, status

from app.v1.schemas.user_api_key import (
    UserApiKeyListRead,
    UserApiKeyRead,
    UserApiKeyCreate,
    UserApiKeyUpdate,
    UserApiKeySearchParams,
)

router = APIRouter()


@router.get(
    "",
    response_model=UserApiKeyListRead,
    name="user_api_keys:list_user_api_keys",
)
async def list_user_api_keys(
    request: Request,
    search_params: UserApiKeySearchParams = Depends(),
):
    """
    Retrieve a list of user API keys with filtering, sorting, and pagination.
    """
    # return await user_api_key_service.get_list(request=request)


@router.post(
    "",
    response_model=UserApiKeyRead,
    status_code=status.HTTP_201_CREATED,
    name="user_api_keys:create_user_api_key",
)
async def create_user_api_key(
    request: Request,
    user_api_key_create: UserApiKeyCreate,
):
    """
    Create a new user API key.
    """
    # return await user_api_key_service.create(request=request, user_api_key_create=user_api_key_create)


@router.patch(
    "/{user_api_key_id}",
    response_model=UserApiKeyRead,
    name="user_api_keys:update_user_api_key",
)
async def update_user_api_key(
    request: Request,
    user_api_key_id: str,
    user_api_key_update: UserApiKeyUpdate,
):
    """
    Update an existing user API key.
    """
    # return await user_api_key_service.update(request=request, user_api_key_id=user_api_key_id, user_api_key_update=user_api_key_update)


@router.delete(
    "/{user_api_key_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    name="user_api_keys:delete_user_api_key",
)
async def delete_user_api_key(
    request: Request,
    user_api_key_id: str,
):
    """
    Delete a user API key.
    """
    # await user_api_key_service.delete(request=request, user_api_key_id=user_api_key_id)
