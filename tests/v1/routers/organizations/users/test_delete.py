import pytest

from httpx import AsyncClient
from app.lib.utils.convert_id import encode_id

from tests.common.check_error_response import check_api_exception_response
from app.lib.error_code import ErrorCode
from fastapi import status


@pytest.mark.asyncio
async def test_delete_user_organization_with_users(
    auth_client: AsyncClient, organization_with_users, user
):
    response = await auth_client.delete(
        f"/organizations/{encode_id(organization_with_users.id)}/users/{user.id}"
    )
    # Assert
    assert response.status_code == 200
    response_data = response.json()
    assert response_data is None


@pytest.mark.asyncio
async def test_delete_user_organization_last_one_user(
    auth_client: AsyncClient, organization, user
):
    response = await auth_client.delete(
        f"/organizations/{encode_id(organization.id)}/users/{user.id}"
    )
    # Assert
    assert response.status_code == 422
    check_api_exception_response(
        response,
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail_code=ErrorCode.ORGANIZATION_LAST_USER_CANNOT_BE_DELETED,
    )


@pytest.mark.asyncio
async def test_delete_user_not_found(
    auth_client: AsyncClient, organization, other_user
):
    response = await auth_client.delete(
        f"/organizations/{encode_id(organization.id)}/users/{other_user.id}"
    )
    # Assert
    assert response.status_code == 404
    check_api_exception_response(
        response, status_code=status.HTTP_404_NOT_FOUND, detail_code=ErrorCode.NOT_FOUND
    )


@pytest.mark.asyncio
async def test_delete_org_not_found(auth_client: AsyncClient, fake_id, user):
    response = await auth_client.delete(f"/organizations/{fake_id}/users/{user.id}")
    # Assert
    assert response.status_code == 404
    check_api_exception_response(
        response, status_code=status.HTTP_404_NOT_FOUND, detail_code=ErrorCode.NOT_FOUND
    )
