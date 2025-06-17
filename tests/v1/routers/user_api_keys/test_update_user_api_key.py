import pytest

from httpx import AsyncClient
from tests.common.check_error_response import (
    check_unauthorized_response,
    check_validation_error_response,
)
from app.v1.schemas.user_api_key.write import UserApiKeyUpdate, UserApiKeyCreate


@pytest.mark.asyncio
async def test_update_user_api_key_unauthenticated(client: AsyncClient):
    """
    Test that unauthenticated requests return 401 Unauthorized.
    """
    response = await client.patch("/user-api-keys/test")
    check_unauthorized_response(response)


@pytest.mark.asyncio
async def test_update_user_api_key(auth_client: AsyncClient):
    """
    Test that a user can update their API key.
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
    user_api_key_update = UserApiKeyUpdate(
        name="Updated API Key",
        expires_at=None,
        allowed_origin=None,
        allowed_ip=None,
    )
    response = await auth_client.patch(
        f"/user-api-keys/{user_api_key['id']}", json=user_api_key_update.model_dump()
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["name"] == user_api_key_update.name
    assert response_json["expires_at"] == user_api_key_update.expires_at


@pytest.mark.asyncio
async def test_update_user_api_key_invalid(auth_client: AsyncClient):
    """
    Test that a user can update their API key.
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
    user_api_key_update = UserApiKeyUpdate.model_construct(
        name="",  # Invalid name
        expires_at=None,
        allowed_origin=None,
        allowed_ip=None,
    )
    response = await auth_client.patch(
        f"/user-api-keys/{user_api_key['id']}", json=user_api_key_update.model_dump()
    )
    check_validation_error_response(
        response,
        path=f"/user-api-keys/{user_api_key['id']}",
        errors=[
            {
                "code": "validation_error",
                "title": "Validation Error",
                "detail": "String should have at least 1 character",
                "source": {"pointer": "#/name"},
            }
        ],
    )
