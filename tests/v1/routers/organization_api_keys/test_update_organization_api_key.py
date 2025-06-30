import pytest

from httpx import AsyncClient
from tests.common.check_error_response import (
    check_api_exception_response,
)
from fastapi import status
from app.v1.schemas.organization_api_key.write import (
    OrganizationApiKeyUpdate,
)
from app.lib.error_code import ErrorCode

from app.lib.utils.convert_id import encode_id


@pytest.mark.asyncio
async def test_update_organization_api_key(
    auth_client: AsyncClient, organization, organization_api_key
):
    organization_api_key_update = OrganizationApiKeyUpdate(
        name="Updated API Key",
        expires_at=None,
        allowed_origin=None,
        allowed_ip=None,
    )
    response = await auth_client.patch(
        f"/organizations/{encode_id(organization.id)}/api-keys/{encode_id(organization_api_key.id)}",
        json=organization_api_key_update.model_dump(),
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["name"] == organization_api_key_update.name
    assert response_json["expires_at"] == organization_api_key_update.expires_at


@pytest.mark.asyncio
async def test_update_organization_api_key_invalid(
    auth_client: AsyncClient, organization, organization_api_key
):
    organization_api_key_update = OrganizationApiKeyUpdate.model_construct(
        name="",  # Invalid name
        expires_at=None,
        allowed_origin=None,
        allowed_ip=None,
    )
    response = await auth_client.patch(
        f"/organizations/{encode_id(organization.id)}/api-keys/{encode_id(organization_api_key.id)}",
        json=organization_api_key_update.model_dump(),
    )
    check_api_exception_response(
        response,
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail_code=ErrorCode.VALIDATION_ERROR,
        detail_detail="String should have at least 1 character",
        pointer="name",
    )
