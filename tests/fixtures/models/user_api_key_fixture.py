import pytest_asyncio
from datetime import datetime, timedelta


@pytest_asyncio.fixture
async def user_api_key(async_session, user, user_api_key_factory):
    user_api_key = await user_api_key_factory.create(user=user)
    return user_api_key


@pytest_asyncio.fixture
async def expired_user_api_key(async_session, user, user_api_key_factory):
    user_api_key = await user_api_key_factory.create(
        user=user, expires_at=datetime.utcnow() - timedelta(days=1)
    )
    return user_api_key


@pytest_asyncio.fixture
async def soft_deleted_user_api_key(async_session, user, user_api_key_factory):
    user_api_key = await user_api_key_factory.create(
        user=user, deleted_at=datetime.utcnow()
    )
    return user_api_key


@pytest_asyncio.fixture
async def user_api_keys(async_session, user, user_api_key_factory):
    user_api_keys = await user_api_key_factory.create_batch(size=10, user=user)
    return user_api_keys
