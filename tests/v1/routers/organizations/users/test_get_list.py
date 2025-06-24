import pytest

from httpx import AsyncClient
from app.lib.utils.convert_id import encode_id

from tests.common.check_error_response import check_api_exception_response
from app.lib.error_code import ErrorCode
from fastapi import status


@pytest.mark.asyncio
async def test_get_list_organization(auth_client: AsyncClient, organization):
    response = await auth_client.get(
        f"/organizations/{encode_id(organization.id)}/users"
    )
    # Assert
    assert response.status_code == 200
    response_data = response.json()["data"]
    assert isinstance(response_data, list)
    assert len(response_data) > 0

    # Check the structure of the first user in the list
    first_user = response_data[0]
    assert "id" in first_user
    assert "email" in first_user


@pytest.mark.asyncio
async def test_get_list_organization_with_limit(auth_client: AsyncClient, organization):
    response = await auth_client.get(
        f"/organizations/{encode_id(organization.id)}/users",
        params={"limit": 3, "offset": 0, "sorted_by": "email", "sorted_order": "asc"},
    )
    # Assert
    assert response.status_code == 200
    response_data = response.json()["data"]
    assert isinstance(response_data, list)
    assert len(response_data) > 0

    # Check the structure of the first user in the list
    first_user = response_data[0]
    assert "id" in first_user
    assert "email" in first_user


@pytest.mark.asyncio
async def test_get_list_organization_filtered(
    auth_client: AsyncClient, organization_with_users, user
):
    response = await auth_client.get(
        f"/organizations/{encode_id(organization_with_users.id)}/users",
        params={"email__icontains": user.email},
    )
    # Assert
    assert response.status_code == 200
    response_data = response.json()["data"]
    assert isinstance(response_data, list)
    assert len(response_data) == 1

    # Check the structure of the first user in the list
    first_user = response_data[0]
    assert "id" in first_user
    assert "email" in first_user
    assert first_user["email"] == user.email


@pytest.mark.asyncio
async def test_get_list_organization_not_found(auth_client: AsyncClient, fake_id):
    response = await auth_client.get(f"/organizations/{fake_id}/users")
    # Assert
    assert response.status_code == 404
    check_api_exception_response(
        response, status_code=status.HTTP_404_NOT_FOUND, detail_code=ErrorCode.NOT_FOUND
    )
