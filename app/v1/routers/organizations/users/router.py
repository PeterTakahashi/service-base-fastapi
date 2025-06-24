from fastapi import Depends, status
from app.v1.schemas.organization import (
    OrganizationRead,
)
from app.v1.schemas.organization.invite import (
    OrganizationUserInvite,
)
from app.v1.dependencies.models.organization.get_organization_by_id import (
    get_organization_by_id,
)
from app.models.organization import Organization
from app.core.routers.auth_api_router import AuthAPIRouter
from app.lib.fastapi_users.user_setup import current_active_user
from app.models.user import User

from .response_type import INVITE_RESPONSES

router = AuthAPIRouter(
    prefix="/organizations/{organization_id}/invite",
    tags=["Organization User Invitation"],
)


@router.post(
    "",
    response_model=OrganizationRead,
    name="organizations:users:invite",
    status_code=status.HTTP_201_CREATED,
    responses=INVITE_RESPONSES,
)
async def invite(
    params: OrganizationUserInvite,
    organization: Organization = Depends(get_organization_by_id),
) -> None:
    return None


@router.post(
    "/accept",
    response_model=OrganizationRead,
    name="organizations:users:invite:accept",
    status_code=status.HTTP_201_CREATED,
)
async def accept_invitation(
    user: User = Depends(current_active_user),
    organization: Organization = Depends(get_organization_by_id),
) -> None:
    return None
