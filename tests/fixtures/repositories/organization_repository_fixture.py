import pytest_asyncio
from app.v1.repositories.organization_repository import OrganizationRepository


@pytest_asyncio.fixture
async def organization_repository(async_session):
    return OrganizationRepository(async_session)
