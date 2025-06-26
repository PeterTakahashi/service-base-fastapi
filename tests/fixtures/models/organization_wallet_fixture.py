import pytest_asyncio


@pytest_asyncio.fixture
async def organization_wallet(
    async_session, organization_wallet_repository, organization
):
    organization_wallet = await organization_wallet_repository.find_by(
        organization_id=organization.id
    )
    return organization_wallet


@pytest_asyncio.fixture
async def other_organization_wallet(
    async_session, organization_wallet_repository, other_organization
):
    organization_wallet = await organization_wallet_repository.find_by(
        organization_id=other_organization.id
    )
    return organization_wallet


@pytest_asyncio.fixture
async def organization_wallets(
    async_session, organization_wallet_repository, organizations
):
    organization_wallets = []
    for organization in organizations:
        organization_wallet = await organization_wallet_repository.find_by(
            organization_id=organization.id
        )
        organization_wallets.append(organization_wallet)
    return organization_wallets
