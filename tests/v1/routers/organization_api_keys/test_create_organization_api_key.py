import pytest

from httpx import AsyncClient
from app.v1.schemas.organization_api_key.write import OrganizationApiKeyCreate

from app.lib.utils.convert_id import encode_id

@pytest.mark.asyncio
async def test_create_organization_api_key(
    auth_client: AsyncClient,
    organization,
):
    """
    Test that a organization can create an API key.
    """
    organization_api_key_create = OrganizationApiKeyCreate(
        name="Test API Key",
        expires_at=None,
        allowed_origin=None,
        allowed_ip=None,
    )
    response = await auth_client.post(
        f"/organizations/{encode_id(organization.id)}/api-keys",
        json=organization_api_key_create.model_dump(),
    )
    assert response.status_code == 201
    assert response.json()["name"] == organization_api_key_create.name


@pytest.mark.asyncio
async def test_create_organization_validation_error_organization_api_key(
    auth_client: AsyncClient,
    organization,
):
    """
    Test that creating an API key with invalid data returns a validation error.
    """
    organization_api_key_create = OrganizationApiKeyCreate.model_construct(
        name="",  # Invalid name
        expires_at=None,
    )
    response = await auth_client.post(
        f"/organizations/{encode_id(organization.id)}/api-keys",
        json=organization_api_key_create.model_dump(),
    )
    assert response.status_code == 422
