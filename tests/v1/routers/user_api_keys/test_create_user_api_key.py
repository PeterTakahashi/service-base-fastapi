import pytest

from httpx import AsyncClient
from tests.common.check_error_response import check_unauthorized_response
from app.v1.schemas.user_api_key.write import UserApiKeyCreate


@pytest.mark.asyncio
async def test_create_user_api_key_unauthenticated(client: AsyncClient):
    """
    Test that unauthenticated requests return 401 Unauthorized.
    """
    response = await client.post("/user-api-keys")
    check_unauthorized_response(
        response, path="/user-api-keys"
    )


@pytest.mark.asyncio
async def test_create_user_api_key(
    auth_client: AsyncClient,
):
    """
    Test that a user can create an API key.
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
    assert response.json()["name"] == user_api_key_create.name


@pytest.mark.asyncio
async def test_create_user_validation_error_user_api_key(
    auth_client: AsyncClient,
):
    """
    Test that creating an API key with invalid data returns a validation error.
    """
    user_api_key_create = UserApiKeyCreate.model_construct(
        name="",  # Invalid name
        expires_at=None,
    )
    response = await auth_client.post(
        "/user-api-keys", json=user_api_key_create.model_dump()
    )
    assert response.status_code == 422
