import pytest_asyncio


@pytest_asyncio.fixture
async def user_wallet(async_session, user_wallet_factory, user):
    user_wallet = await user_wallet_factory.create(user=user)
    return user_wallet


@pytest_asyncio.fixture
async def other_user_wallet(async_session, user_wallet_factory, other_user):
    user_wallet = await user_wallet_factory.create(user=other_user)
    return user_wallet


@pytest_asyncio.fixture
async def user_wallets(async_session, user_wallet_factory, users):
    user_wallets = []
    for user in users:
        user_wallet = await user_wallet_factory.create(user=user)
        user_wallets.append(user_wallet)
    return user_wallets
