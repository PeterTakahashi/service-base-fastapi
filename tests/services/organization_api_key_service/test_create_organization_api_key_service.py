import pytest
from app.v1.schemas.organization_api_key import (
    OrganizationApiKeyCreate,
    OrganizationApiKeyRead,
)
from datetime import datetime, timedelta


@pytest.mark.asyncio
async def test_create_organization_api_key_service(
    organization_api_key_service, user, organization
):
    organization_api_key_create = OrganizationApiKeyCreate(
        name="Test API Key",
        expires_at=datetime.utcnow() + timedelta(days=30),
    )
    organization_api_key = await organization_api_key_service.create(
        user_id=user.id,
        organization_id=organization.id,
        organization_api_key_create=organization_api_key_create,
    )
    assert organization_api_key
    assert isinstance(organization_api_key, OrganizationApiKeyRead)
    assert organization_api_key.name == organization_api_key_create.name
    assert organization_api_key.expires_at == organization_api_key_create.expires_at
    assert organization_api_key.api_key is not None
    assert organization_api_key.created_by_user.id == user.id
