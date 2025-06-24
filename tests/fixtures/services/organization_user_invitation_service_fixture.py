import pytest_asyncio
from app.v1.services.organization_user_invitation_service import (
    OrganizationUserInvitationService,
)
from app.lib.utils.mailer import mailer


@pytest_asyncio.fixture
async def organization_user_invitation_service(
    organization_repository,
    user_organization_assignment_repository,
    user_organization_invitation_repository,
    user_repository,
):
    return OrganizationUserInvitationService(
        organization_repository,
        user_organization_assignment_repository,
        user_organization_invitation_repository,
        user_repository,
        mailer,
    )
