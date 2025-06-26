import pytest_asyncio

@pytest_asyncio.fixture
async def user(async_session, user_factory, user_address_factory):
    user = await user_factory.create()
    await user_address_factory.create(user_id=user.id)
    return user


@pytest_asyncio.fixture
async def other_user(async_session, user_factory, user_address_factory):
    user = await user_factory.create()
    await user_address_factory.create(user_id=user.id)
    return user


@pytest_asyncio.fixture
async def users(async_session, user_factory, user_address_factory):
    users = await user_factory.create_batch(size=10)
    for user in users:
        await user_address_factory.create(user_id=user.id)
    return users
