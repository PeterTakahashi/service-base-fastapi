import pytest_asyncio


@pytest_asyncio.fixture
async def organization_wallet_transaction(
    async_session, organization_wallet, organization_wallet_transaction_factory
):
    transaction = await organization_wallet_transaction_factory.create(
        organization_wallet=organization_wallet
    )
    return transaction


@pytest_asyncio.fixture
async def other_organization_wallet_transaction(
    async_session, other_organization_wallet, organization_wallet_transaction_factory
):
    transaction = await organization_wallet_transaction_factory.create(
        organization_wallet=other_organization_wallet
    )
    return transaction
