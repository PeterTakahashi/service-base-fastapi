from fastapi import Depends, Request, status

from app.v1.schemas.organization_api_key import (
    OrganizationApiKeyListRead,
    OrganizationApiKeyRead,
    OrganizationApiKeyCreate,
    OrganizationApiKeyUpdate,
    OrganizationApiKeySearchParams,
)
from app.v1.dependencies.services.organization_api_key_service import (
    get_organization_api_key_service,
)
from app.v1.dependencies.models.organization_api_key.get_organization_api_key import (
    get_organization_api_key,
)
from app.v1.services.organization_api_key_service import OrganizationApiKeyService
from app.v1.dependencies.models.organization.get_organization_by_id import (
    get_organization_by_id,
)
from app.models.organization import Organization
from app.models.organization_api_key import OrganizationApiKey

from app.core.routers.auth_api_router import AuthAPIRouter

from app.lib.fastapi_users.user_setup import current_active_user
from app.models.user import User

router = AuthAPIRouter(prefix="/organization-api-keys", tags=["Organization API Keys"])


@router.get(
    "",
    response_model=OrganizationApiKeyListRead,
    name="organization_api_keys:list_organization_api_keys",
)
async def list_organization_api_keys(
    request: Request,
    search_params: OrganizationApiKeySearchParams = Depends(),
    organization: Organization = Depends(get_organization_by_id),
    service: OrganizationApiKeyService = Depends(get_organization_api_key_service),
):
    """
    Retrieve a list of organization API keys with filtering, sorting, and pagination.
    """
    return await service.get_list(
        organization_id=organization.id, search_params=search_params
    )


@router.get(
    "/{organization_api_key_id}",
    response_model=OrganizationApiKeyRead,
    name="organization_api_keys:get_organization_api_keys",
)
async def get_organization_api_keys(
    organization_api_key: OrganizationApiKey = Depends(get_organization_api_key),
):
    """
    Retrieve a organization API key by its ID.
    """
    return OrganizationApiKeyRead.model_validate(organization_api_key)


@router.post(
    "",
    response_model=OrganizationApiKeyRead,
    status_code=status.HTTP_201_CREATED,
    name="organization_api_keys:create_organization_api_key",
)
async def create_organization_api_key(
    request: Request,
    organization_api_key_create: OrganizationApiKeyCreate,
    organization: Organization = Depends(get_organization_by_id),
    service: OrganizationApiKeyService = Depends(get_organization_api_key_service),
    user: User = Depends(current_active_user),
):
    """
    Create a new organization API key.
    """
    return await service.create(
        user_id=user.id,
        organization_id=organization.id,
        organization_api_key_create=organization_api_key_create,
    )


@router.patch(
    "/{organization_api_key_id}",
    response_model=OrganizationApiKeyRead,
    name="organization_api_keys:update_organization_api_key",
)
async def update_organization_api_key(
    request: Request,
    organization_api_key_update: OrganizationApiKeyUpdate,
    organization_api_key: OrganizationApiKey = Depends(get_organization_api_key),
    service: OrganizationApiKeyService = Depends(get_organization_api_key_service),
):
    """
    Update an existing organization API key.
    """
    return await service.update(
        organization_api_key_id=organization_api_key.id,
        organization_api_key_update=organization_api_key_update,
    )


@router.delete(
    "/{organization_api_key_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    name="organization_api_keys:delete_organization_api_key",
)
async def delete_organization_api_key(
    request: Request,
    organization_api_key: OrganizationApiKey = Depends(get_organization_api_key),
    service: OrganizationApiKeyService = Depends(get_organization_api_key_service),
) -> None:
    """
    Delete a organization API key.
    """
    await service.delete(organization_api_key_id=organization_api_key.id)
    return None
