import pytest

from httpx import AsyncClient
from fastapi import status
from tests.common.check_error_response import check_api_exception_response
from app.v1.schemas.user_api_key.write import UserApiKeyCreate

from app.lib.convert_id import encode_id


@pytest.mark.asyncio
async def test_delete_user_api_key_unauthenticated(client: AsyncClient):
    """
    Test that unauthenticated requests return 401 Unauthorized.
    """
    response = await client.delete("/user-api-keys/test")
    check_api_exception_response(
        response, status_code=status.HTTP_401_UNAUTHORIZED, detail_code="unauthorized"
    )


@pytest.mark.asyncio
async def test_delete_user_api_key(auth_client: AsyncClient):
    """
    Test that a user can delete their API key.
    """
    user_api_key_create = UserApiKeyCreate(
        name="Test API Key",
        expires_at=None,
        allowed_origin=None,
        allowed_ip=None,
    )
    create_response = await auth_client.post(
        "/user-api-keys", json=user_api_key_create.model_dump()
    )
    user_api_key = create_response.json()
    response = await auth_client.delete(f"/user-api-keys/{user_api_key['id']}")
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_update_user_api_key_not_found(auth_client: AsyncClient):
    """
    Test that deleting a non-existent API key returns 404 Not Found.
    """
    response = await auth_client.delete(f"/user-api-keys/{encode_id(0)}")
    assert response.status_code == 404
