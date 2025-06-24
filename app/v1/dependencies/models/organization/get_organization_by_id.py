from fastapi import Depends
from app.models.user import User
from app.models.organization import Organization
from app.v1.repositories.organization_repository import OrganizationRepository
from app.v1.dependencies.repositories.organization_repository import (
    get_organization_repository,
)
from app.v1.repositories.user_organization_assignment_repository import (
    UserOrganizationAssignmentRepository,
)
from app.v1.dependencies.repositories.user_organization_assignment_repository import (
    get_user_organization_assignment_repository,
)
from app.lib.fastapi_users.user_setup import current_active_user
from app.lib.utils.convert_id import decode_id


async def get_not_assigned_organization_by_id(
    organization_id: str,
    organization_repository: OrganizationRepository = Depends(
        get_organization_repository
    ),
    user: User = Depends(current_active_user),
) -> Organization:
    organization = await organization_repository.find_by_or_raise(
        id=decode_id(organization_id)
    )
    return organization


async def get_organization_by_id(
    organization_id: str,
    organization_repository: OrganizationRepository = Depends(
        get_organization_repository
    ),
    user_organization_assignment_repository: UserOrganizationAssignmentRepository = Depends(
        get_user_organization_assignment_repository
    ),
    user: User = Depends(current_active_user),
) -> Organization:
    organization = await organization_repository.find_by_or_raise(
        id=decode_id(organization_id)
    )
    await user_organization_assignment_repository.find_by_or_raise(
        user_id=user.id, organization_id=organization.id
    )
    return organization
