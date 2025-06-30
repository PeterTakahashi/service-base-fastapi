import pytest

from httpx import AsyncClient
from app.lib.utils.convert_id import encode_id

from tests.common.check_error_response import check_api_exception_response
from app.lib.error_code import ErrorCode
from fastapi import status


@pytest.mark.asyncio
async def test_get_user_organization(auth_client: AsyncClient, organization, user):
    response = await auth_client.get(
        f"/organizations/{encode_id(organization.id)}/users/{user.id}"
    )
    # Assert
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["id"] == str(user.id)
    assert response_data["email"] == user.email


@pytest.mark.asyncio
async def test_get_user_not_found(auth_client: AsyncClient, organization, other_user):
    response = await auth_client.get(
        f"/organizations/{encode_id(organization.id)}/users/{other_user.id}"
    )
    # Assert
    assert response.status_code == 404
    check_api_exception_response(
        response, status_code=status.HTTP_404_NOT_FOUND, detail_code=ErrorCode.NOT_FOUND
    )


@pytest.mark.asyncio
async def test_get_org_not_found(auth_client: AsyncClient, fake_id, user):
    response = await auth_client.get(f"/organizations/{fake_id}/users/{user.id}")
    # Assert
    assert response.status_code == 404
    check_api_exception_response(
        response, status_code=status.HTTP_404_NOT_FOUND, detail_code=ErrorCode.NOT_FOUND
    )
