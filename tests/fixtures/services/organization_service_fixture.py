import pytest_asyncio
from app.v1.services.organization_service import OrganizationService


@pytest_asyncio.fixture
async def organization_service(
    organization_repository,
    user_organization_assignment_repository,
    organization_wallet_repository,
    organization_address_repository,
):
    return OrganizationService(
        organization_repository,
        user_organization_assignment_repository,
        organization_wallet_repository,
        organization_address_repository,
    )
