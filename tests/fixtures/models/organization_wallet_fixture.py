import pytest_asyncio


@pytest_asyncio.fixture
async def organization_wallet(async_session, organization_wallet_factory, organization):
    organization_wallet = await organization_wallet_factory.create(
        organization=organization
    )
    return organization_wallet


@pytest_asyncio.fixture
async def other_organization_wallet(
    async_session, organization_wallet_factory, other_organization
):
    organization_wallet = await organization_wallet_factory.create(
        organization=other_organization
    )
    return organization_wallet


@pytest_asyncio.fixture
async def organization_wallets(
    async_session, organization_wallet_factory, organizations
):
    organization_wallets = []
    for organization in organizations:
        organization_wallet = await organization_wallet_factory.create(
            organization=organization
        )
        organization_wallets.append(organization_wallet)
    return organization_wallets
