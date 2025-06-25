import pytest_asyncio


@pytest_asyncio.fixture
async def organization_wallet(organization_wallet_repository, organization):
    organization_wallet = await organization_wallet_repository.find_by(
        organization_id=organization.id
    )
    return organization_wallet
