from fastapi import Depends, status
from app.v1.schemas.organization.invite import (
    OrganizationUserInvite,
)
from app.v1.dependencies.models.organization.get_organization_by_id import (
    get_organization_by_id,
    get_not_assigned_organization_by_id,
)
from app.models.organization import Organization
from app.core.routers.auth_api_router import AuthAPIRouter
from app.lib.fastapi_users.user_setup import current_active_user
from app.models.user import User
from app.v1.dependencies.services.organization_user_invitation_service import (
    OrganizationUserInvitationService,
)
from app.v1.dependencies.services.organization_user_invitation_service import (
    get_organization_user_invitation_service,
)

from .response_type import INVITE_RESPONSES

router = AuthAPIRouter(
    prefix="/organizations/{organization_id}/invite",
    tags=["Organization User Invitation"],
)


@router.post(
    "",
    name="organizations:users:invite",
    status_code=status.HTTP_200_OK,
    responses=INVITE_RESPONSES,
)
async def invite(
    params: OrganizationUserInvite,
    organization: Organization = Depends(get_organization_by_id),
    user: User = Depends(current_active_user),
    service: OrganizationUserInvitationService = Depends(
        get_organization_user_invitation_service
    ),
) -> None:
    return await service.invite_user(
        user=user,
        organization=organization,
        user_email=params.email,
    )


@router.patch(
    "/accept",
    name="organizations:users:invite:accept",
    status_code=status.HTTP_200_OK,
)
async def accept_invitation(
    user: User = Depends(current_active_user),
    organization: Organization = Depends(get_not_assigned_organization_by_id),
    service: OrganizationUserInvitationService = Depends(
        get_organization_user_invitation_service
    ),
) -> None:
    return await service.accept_invitation(
        user=user,
        organization=organization,
    )
