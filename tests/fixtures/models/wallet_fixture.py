import pytest_asyncio


@pytest_asyncio.fixture
async def wallet(async_session, wallet_factory, user):
    wallet = await wallet_factory.create(user=user)
    return wallet


@pytest_asyncio.fixture
async def other_wallet(async_session, wallet_factory, other_user):
    wallet = await wallet_factory.create(user=other_user)
    return wallet


@pytest_asyncio.fixture
async def wallets(async_session, wallet_factory, users):
    wallets = []
    for user in users:
        wallet = await wallet_factory.create(user=user)
        wallets.append(wallet)
    return wallets
