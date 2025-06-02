import pytest_asyncio


@pytest_asyncio.fixture
async def user(async_session, user_factory):
    user = await user_factory.create()
    return user


@pytest_asyncio.fixture
async def other_user(async_session, user_factory):
    user = await user_factory.create()
    return user


@pytest_asyncio.fixture
async def users(async_session, user_factory):
    users = await user_factory.create_batch(size=10)
    return users
