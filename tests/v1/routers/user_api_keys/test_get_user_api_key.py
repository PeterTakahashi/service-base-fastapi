import pytest

from httpx import AsyncClient
from fastapi import status
from tests.common.check_error_response import check_api_exception_response
from app.v1.schemas.user_api_key.write import UserApiKeyCreate


@pytest.mark.asyncio
async def test_get_user_api_key_unauthenticated(client: AsyncClient):
    """
    Test that unauthenticated requests return 401 Unauthorized.
    """
    response = await client.get("/user-api-keys/test")
    check_api_exception_response(
        response, status_code=status.HTTP_401_UNAUTHORIZED, detail_code="unauthorized"
    )


@pytest.mark.asyncio
async def test_get_user_api_key(auth_client: AsyncClient):
    """
    Test that a user can retrieve their API key by ID.
    """
    user_api_key_create = UserApiKeyCreate(
        name="Test API Key",
        expires_at=None,
        allowed_origin=None,
        allowed_ip=None,
    )
    response = await auth_client.post(
        "/user-api-keys", json=user_api_key_create.model_dump()
    )
    assert response.status_code == 201
    response_json = response.json()
    user_api_key_id = response_json["id"]

    response = await auth_client.get(f"/user-api-keys/{user_api_key_id}")
    assert response.status_code == 200
    response_json = response.json()

    assert response_json["id"] == str(user_api_key_id)
    assert response_json["name"] == user_api_key_create.name
    assert response_json["api_key"] is not None


@pytest.mark.asyncio
async def test_get_user_api_key_not_found(auth_client: AsyncClient):
    """
    Test that requesting a non-existent API key returns a 404 Not Found.
    """
    response = await auth_client.get("/user-api-keys/nonexistent-id")
    assert response.status_code == 404
    response_json = response.json()
    assert (
        response_json["errors"][0]["detail"]
        == "The requested resource could not be found."
    )
