import pytest

from httpx import AsyncClient
from fastapi import status
from tests.common.check_error_response import check_api_exception_response
from app.lib.error_code import ErrorCode

from app.lib.utils.convert_id import encode_id


@pytest.mark.asyncio
async def test_get_organization_api_key(
    auth_client: AsyncClient, organization, organization_api_key
):
    response = await auth_client.get(
        f"/organizations/{encode_id(organization.id)}/api-keys/{encode_id(organization_api_key.id)}"
    )
    assert response.status_code == 200
    response_json = response.json()

    assert response_json["id"] == encode_id(organization_api_key.id)
    assert response_json["name"] == organization_api_key.name
    assert response_json["api_key"] is not None


@pytest.mark.asyncio
async def test_get_organization_api_key_not_found(
    auth_client: AsyncClient, organization
):
    """
    Test that requesting a non-existent API key returns a 404 Not Found.
    """
    response = await auth_client.get(
        f"/organizations/{encode_id(organization.id)}/api-keys/{encode_id(0)}"
    )
    check_api_exception_response(
        response, status_code=status.HTTP_404_NOT_FOUND, detail_code=ErrorCode.NOT_FOUND
    )
