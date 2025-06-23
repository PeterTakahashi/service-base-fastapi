import pytest_asyncio
from datetime import datetime


@pytest_asyncio.fixture
async def organization(organization_factory, user):
    organization = await organization_factory.create(
        created_by_user_id=user.id,
    )
    return organization


@pytest_asyncio.fixture
async def soft_deleted_organization(organization_factory, user):
    organization = await organization_factory.create(
        created_by_user_id=user.id,
        deleted_at=datetime.utcnow(),
    )
    return organization


@pytest_asyncio.fixture
async def organizations(organization_factory, user):
    organizations = await organization_factory.create_batch(
        5,
        created_by_user_id=user.id,
    )
    return organizations
