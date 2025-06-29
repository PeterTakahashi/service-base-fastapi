import pytest_asyncio
from app.v1.repositories.organization_address_repository import (
    OrganizationAddressRepository,
)


@pytest_asyncio.fixture
async def organization_address_repository(async_session):
    return OrganizationAddressRepository(async_session)
