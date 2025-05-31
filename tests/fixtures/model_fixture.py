import pytest_asyncio


@pytest_asyncio.fixture
async def user(async_session, user_factory):
    user = await user_factory.create()
    return user


@pytest_asyncio.fixture
async def users(async_session, user_factory):
    users = await user_factory.create_batch(size=10)
    return users


@pytest_asyncio.fixture
async def wallet(async_session, wallet_factory, user):
    wallet = await wallet_factory.create(user=user)
    return wallet


@pytest_asyncio.fixture
async def wallets(async_session, wallet_factory, users):
    wallets = []
    for user in users:
        wallet = await wallet_factory.create(user=user)
        wallets.append(wallet)
    return wallets


@pytest_asyncio.fixture
async def wallet_transaction(async_session, wallet, wallet_transaction_factory):
    transaction = await wallet_transaction_factory.create(wallet=wallet)
    return transaction
