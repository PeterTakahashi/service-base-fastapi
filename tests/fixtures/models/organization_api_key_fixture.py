import pytest_asyncio
from datetime import datetime, timedelta


@pytest_asyncio.fixture
async def organization_api_key(
    async_session, organization, organization_api_key_factory
):
    organization_api_key = await organization_api_key_factory.create(
        organization=organization,
        allowed_ip=None,
        allowed_origin=None,
    )
    return organization_api_key


@pytest_asyncio.fixture
async def organization_api_key_with_expires_at(
    async_session, organization, organization_api_key_factory
):
    organization_api_key = await organization_api_key_factory.create(
        organization=organization,
        expires_at=datetime.utcnow() + timedelta(days=1),
        allowed_ip=None,
        allowed_origin=None,
    )
    return organization_api_key


@pytest_asyncio.fixture
async def expired_organization_api_key(
    async_session, organization, organization_api_key_factory
):
    organization_api_key = await organization_api_key_factory.create(
        organization=organization,
        expires_at=datetime.utcnow() - timedelta(days=1),
        allowed_ip=None,
        allowed_origin=None,
    )
    return organization_api_key


@pytest_asyncio.fixture
async def soft_deleted_organization_api_key(
    async_session, organization, organization_api_key_factory
):
    organization_api_key = await organization_api_key_factory.create(
        organization=organization,
        deleted_at=datetime.utcnow(),
        allowed_ip=None,
        allowed_origin=None,
    )
    return organization_api_key


@pytest_asyncio.fixture
async def organization_api_keys(
    async_session, organization, organization_api_key_factory, faker
):
    organization_api_keys = await organization_api_key_factory.create_batch(
        size=10,
        organization=organization,
    )
    return organization_api_keys
