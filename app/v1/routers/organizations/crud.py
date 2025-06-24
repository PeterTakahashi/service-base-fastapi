from fastapi import Depends, Request, status
from app.v1.schemas.organization import (
    OrganizationCreate,
    OrganizationListRead,
    OrganizationRead,
    OrganizationUpdate,
    OrganizationSearchParams,
)
from app.v1.dependencies.models.organization.get_organization_by_id import (
    get_organization_by_id,
)
from app.v1.dependencies.services.organization_service import get_organization_service
from app.v1.services.organization_service import OrganizationService
from app.lib.fastapi_users.user_setup import current_active_user
from app.models.user import User
from app.models.organization import Organization

from app.core.routers.auth_api_router import AuthAPIRouter

router = AuthAPIRouter(prefix="/organizations", tags=["Organizations"])


@router.get(
    "",
    response_model=OrganizationListRead,
    name="organizations:list_organizations",
)
async def list_organizations(
    request: Request,
    search_params: OrganizationSearchParams = Depends(),
    user: User = Depends(current_active_user),
    service: OrganizationService = Depends(get_organization_service),
):
    """
    Retrieve a list of organizations with filtering, sorting, and pagination.
    """
    return await service.get_list(user_id=user.id, search_params=search_params)


@router.get(
    "/{organization_id}",
    response_model=OrganizationRead,
    name="organizations:get_organization",
)
async def get_organization(
    organization: Organization = Depends(get_organization_by_id),
):
    """
    Retrieve an organization by its ID.
    """
    return OrganizationRead.model_validate(organization)


@router.post(
    "",
    response_model=OrganizationRead,
    status_code=status.HTTP_201_CREATED,
    name="organizations:create_organization",
)
async def create_organization(
    request: Request,
    organization_params: OrganizationCreate,
    user: User = Depends(current_active_user),
    service: OrganizationService = Depends(get_organization_service),
):
    """
    Create a new organization.
    """
    return await service.create(organization_params=organization_params, user=user)


@router.put(
    "/{organization_id}",
    response_model=OrganizationRead,
    name="organizations:update_organization",
)
async def update_organization(
    organization_params: OrganizationUpdate,
    organization: Organization = Depends(get_organization_by_id),
    service: OrganizationService = Depends(get_organization_service),
):
    """
    Update an existing organization.
    """
    return await service.update(
        id=organization.id, organization_params=organization_params
    )


@router.delete(
    "/{organization_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    name="organizations:delete_organization",
)
async def delete_organization(
    organization: Organization = Depends(get_organization_by_id),
    user: User = Depends(current_active_user),
    service: OrganizationService = Depends(get_organization_service),
):
    """
    Delete an organization.
    """
    await service.delete(id=organization.id)
    return None
