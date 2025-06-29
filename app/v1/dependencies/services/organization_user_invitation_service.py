from fastapi import Depends
from app.v1.services.organization_user_invitation_service import (
    OrganizationUserInvitationService,
)
from app.v1.repositories.organization_repository import OrganizationRepository
from app.v1.repositories.user_organization_assignment_repository import (
    UserOrganizationAssignmentRepository,
)
from app.v1.repositories.user_organization_invitation_repository import (
    UserOrganizationInvitationRepository,
)
from app.v1.repositories.user_repository import UserRepository

from app.v1.dependencies.repositories.organization_repository import (
    get_organization_repository,
)
from app.v1.dependencies.repositories.user_organization_assignment_repository import (
    get_user_organization_assignment_repository,
)
from app.v1.dependencies.repositories.user_organization_invitation_repository import (
    get_user_organization_invitation_repository,
)
from app.v1.dependencies.repositories.user_repository import get_user_repository
from app.v1.dependencies.mailer import get_mailer
from fastapi_mail import FastMail


def get_organization_user_invitation_service(
    organization_repository: OrganizationRepository = Depends(
        get_organization_repository
    ),
    user_organization_assignment_repository: UserOrganizationAssignmentRepository = Depends(
        get_user_organization_assignment_repository
    ),
    user_organization_invitation_repository: UserOrganizationInvitationRepository = Depends(
        get_user_organization_invitation_repository
    ),
    user_repository: UserRepository = Depends(get_user_repository),
    fast_mail: FastMail = Depends(get_mailer),
) -> OrganizationUserInvitationService:
    return OrganizationUserInvitationService(
        organization_repository=organization_repository,
        user_organization_assignment_repository=user_organization_assignment_repository,
        user_organization_invitation_repository=user_organization_invitation_repository,
        user_repository=user_repository,
        fast_mail=fast_mail,
    )
