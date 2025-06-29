import pytest

from httpx import AsyncClient
from app.lib.utils.convert_id import encode_id
from tests.common.check_error_response import check_api_exception_response
from app.lib.error_code import ErrorCode
from fastapi import status


@pytest.mark.asyncio
async def test_get_organization(
    auth_client: AsyncClient,
    organization,
):
    response = await auth_client.get(f"/organizations/{encode_id(organization.id)}")
    # Assert
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["id"] == encode_id(organization.id)
    assert response_data["name"] == organization.name
    assert response_data["description"] == organization.description
    assert response_data["profile_image_key"] == organization.profile_image_key
    assert response_data["billing_email"] == organization.billing_email


@pytest.mark.asyncio
async def test_get_organization_by_other_user(
    other_auth_client: AsyncClient,
    organization,
):
    response = await other_auth_client.get(f"/organizations/{organization.id}")
    # Assert
    assert response.status_code == 404
    check_api_exception_response(
        response, status_code=status.HTTP_404_NOT_FOUND, detail_code=ErrorCode.NOT_FOUND
    )


@pytest.mark.asyncio
async def test_get_uncreated_organization(
    auth_client: AsyncClient,
    fake_id,
):
    response = await auth_client.get(f"/organizations/{fake_id}")
    # Assert
    assert response.status_code == 404
    check_api_exception_response(
        response, status_code=status.HTTP_404_NOT_FOUND, detail_code=ErrorCode.NOT_FOUND
    )
