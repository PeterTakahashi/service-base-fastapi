import pytest_asyncio
from app.v1.repositories.organization_api_key_repository import (
    OrganizationApiKeyRepository,
)


@pytest_asyncio.fixture
async def organization_api_key_repository(async_session):
    return OrganizationApiKeyRepository(async_session)
