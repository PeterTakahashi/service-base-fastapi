from fastapi import Depends, status
from app.v1.dependencies.models.organization.get_organization_by_id import (
    get_organization_by_id,
)
from app.models.organization import Organization
from app.core.routers.auth_api_router import AuthAPIRouter
from app.lib.fastapi_users.user_setup import current_active_user
from app.models.user import User
from app.v1.dependencies.services.organization_user_service import (
    OrganizationUserService,
)
from app.v1.dependencies.services.organization_user_service import (
    get_organization_user_service,
)
from app.v1.schemas.organization.users.search_params import (
    OrganizationUserSearchParams,
)
from app.v1.schemas.organization.users.read_list import UserListRead
from app.v1.schemas.user.read import UserRead

router = AuthAPIRouter(
    prefix="/organizations/{organization_id}/users",
    tags=["Organization User"],
)


@router.get(
    "",
    name="organizations:users",
    status_code=status.HTTP_200_OK,
    response_model=UserListRead,
)
async def get_list(
    search_params: OrganizationUserSearchParams = Depends(),
    organization: Organization = Depends(get_organization_by_id),
    user: User = Depends(current_active_user),
    service: OrganizationUserService = Depends(get_organization_user_service),
) -> UserListRead:
    return await service.get_list(
        organization_id=organization.id,
        search_params=search_params,
    )

@router.get(
    "/{user_id}",
    name="organizations:user",
    status_code=status.HTTP_200_OK,
    response_model=UserRead,
)
async def get(
    user_id: str,
    organization: Organization = Depends(get_organization_by_id),
    user: User = Depends(current_active_user),
    service: OrganizationUserService = Depends(get_organization_user_service),
) -> UserRead:
    return await service.get(
        organization_id=organization.id,
        user_id=user_id
    )
