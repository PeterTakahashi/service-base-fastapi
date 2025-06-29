import pytest_asyncio
from app.v1.repositories.user_organization_invitation_repository import (
    UserOrganizationInvitationRepository,
)


@pytest_asyncio.fixture
async def user_organization_invitation_repository(async_session):
    return UserOrganizationInvitationRepository(async_session)
