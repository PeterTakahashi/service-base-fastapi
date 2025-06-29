import pytest_asyncio
from app.v1.services.organization_api_key_service import OrganizationApiKeyService


@pytest_asyncio.fixture
async def organization_api_key_service(organization_api_key_repository):
    return OrganizationApiKeyService(organization_api_key_repository)
