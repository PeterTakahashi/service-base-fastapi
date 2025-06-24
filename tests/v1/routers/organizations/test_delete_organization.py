import pytest

from httpx import AsyncClient
from sqlalchemy.exc import NoResultFound
from app.lib.utils.convert_id import encode_id
from tests.common.check_error_response import check_api_exception_response
from app.lib.error_code import ErrorCode
from fastapi import status


@pytest.mark.asyncio
async def test_delete_organization(
    auth_client: AsyncClient,
    organization_repository,
    organization,
):
    # Arrange
    organization_id = organization.id

    # Act
    response = await auth_client.delete(f"/organizations/{encode_id(organization_id)}")

    # Assert
    assert response.status_code == 204

    # Verify the organization is deleted
    with pytest.raises(NoResultFound):
        await organization_repository.find(organization_id)


@pytest.mark.asyncio
async def test_delete_organization_by_other_user(
    other_auth_client: AsyncClient,
    organization,
):
    # Arrange
    organization_id = organization.id

    # Act
    response = await other_auth_client.delete(
        f"/organizations/{encode_id(organization_id)}"
    )

    # Assert
    assert response.status_code == 404
    check_api_exception_response(
        response, status_code=status.HTTP_404_NOT_FOUND, detail_code=ErrorCode.NOT_FOUND
    )


@pytest.mark.asyncio
async def test_delete_uncreated_organization(
    auth_client: AsyncClient,
    fake_id,
):
    # Act
    response = await auth_client.delete(f"/organizations/{fake_id}")

    # Assert
    assert response.status_code == 404
    check_api_exception_response(
        response, status_code=status.HTTP_404_NOT_FOUND, detail_code=ErrorCode.NOT_FOUND
    )
