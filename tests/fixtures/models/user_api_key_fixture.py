import pytest_asyncio
from datetime import datetime, timedelta


@pytest_asyncio.fixture
async def user_api_key(async_session, user, user_api_key_factory):
    user_api_key = await user_api_key_factory.create(
        user=user,
        allowed_ip=None,
        allowed_origin=None,
    )
    return user_api_key


@pytest_asyncio.fixture
async def user_api_key_with_expires_at(async_session, user, user_api_key_factory):
    user_api_key = await user_api_key_factory.create(
        user=user,
        expires_at=datetime.utcnow() + timedelta(days=1),
        allowed_ip=None,
        allowed_origin=None,
    )
    return user_api_key


@pytest_asyncio.fixture
async def expired_user_api_key(async_session, user, user_api_key_factory):
    user_api_key = await user_api_key_factory.create(
        user=user,
        expires_at=datetime.utcnow() - timedelta(days=1),
        allowed_ip=None,
        allowed_origin=None,
    )
    return user_api_key


@pytest_asyncio.fixture
async def soft_deleted_user_api_key(async_session, user, user_api_key_factory):
    user_api_key = await user_api_key_factory.create(
        user=user,
        deleted_at=datetime.utcnow(),
        allowed_ip=None,
        allowed_origin=None,
    )
    return user_api_key


@pytest_asyncio.fixture
async def user_api_keys(async_session, user, user_api_key_factory, faker):
    user_api_keys = await user_api_key_factory.create_batch(
        size=10,
        user=user,
    )
    return user_api_keys
