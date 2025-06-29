import pytest

from httpx import AsyncClient
from fastapi import status
from tests.common.check_error_response import check_api_exception_response

from app.lib.utils.convert_id import encode_id
from app.lib.error_code import ErrorCode


@pytest.mark.asyncio
async def test_delete_organization_api_key(
    auth_client: AsyncClient, organization, organization_api_key
):
    response = await auth_client.delete(
        f"/organizations/{encode_id(organization.id)}/api-keys/{encode_id(organization_api_key.id)}"
    )
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_organization_api_key_not_found(
    auth_client: AsyncClient, organization
):
    """
    Test that deleting a non-existent API key returns 404 Not Found.
    """
    response = await auth_client.delete(
        f"/organizations/{encode_id(organization.id)}/api-keys/{encode_id(0)}"
    )
    check_api_exception_response(
        response, status_code=status.HTTP_404_NOT_FOUND, detail_code=ErrorCode.NOT_FOUND
    )


@pytest.mark.asyncio
async def test_delete_organization_not_found(
    auth_client: AsyncClient, organization_api_key
):
    """
    Test that deleting a non-existent API key returns 404 Not Found.
    """
    response = await auth_client.delete(
        f"/organizations/{encode_id(0)}/api-keys/{encode_id(organization_api_key.id)}"
    )
    check_api_exception_response(
        response, status_code=status.HTTP_404_NOT_FOUND, detail_code=ErrorCode.NOT_FOUND
    )
