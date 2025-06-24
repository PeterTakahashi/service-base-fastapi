import pytest_asyncio
from app.v1.services.organization_user_service import OrganizationUserService


@pytest_asyncio.fixture
async def organization_user_service(
    user_repository, user_organization_assignment_repository
):
    return OrganizationUserService(
        user_repository, user_organization_assignment_repository
    )
