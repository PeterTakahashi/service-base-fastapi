import pytest_asyncio
from app.v1.repositories.user_organization_assignment_repository import (
    UserOrganizationAssignmentRepository,
)


@pytest_asyncio.fixture
async def user_organization_assignment_repository(async_session):
    return UserOrganizationAssignmentRepository(async_session)
