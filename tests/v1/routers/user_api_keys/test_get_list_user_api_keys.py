import pytest

from httpx import AsyncClient
from tests.common.check_error_response import check_unauthorized_response
from app.lib.convert_id import decode_id


@pytest.mark.asyncio
async def test_list_user_api_keys_unauthenticated(client: AsyncClient):
    """
    Test that unauthenticated requests return 401 Unauthorized.
    """
    response = await client.get("/user-api-keys")
    check_unauthorized_response(response)


@pytest.mark.asyncio
async def test_list_user_api_keys_no_filter(
    auth_client: AsyncClient,
    user_api_key_factory,
    user_api_key_repository,
    user_repository,
):
    """
    Test that all user API keys for the authenticated user are returned when no filter is provided.
    """
    users = await user_repository.where()
    user = users[0]
    # Create multiple API keys for the same user
    api_key1 = await user_api_key_factory.create(user=user)
    api_key2 = await user_api_key_factory.create(user=user)

    response = await auth_client.get("/user-api-keys")
    assert response.status_code == 200

    response_json = response.json()
    data = response_json["data"]

    # We expect only api_key1 and api_key2
    returned_ids = sorted(decode_id(api_key["id"]) for api_key in data)
    expected_ids = sorted([api_key1.id, api_key2.id])

    assert returned_ids == expected_ids


@pytest.mark.asyncio
async def test_list_user_api_keys_with_filter(
    auth_client: AsyncClient,
    user_api_key_factory,
    user_api_key_repository,
    user_repository,
):
    """
    Test that user API keys can be filtered by name and api_key.
    """
    users = await user_repository.where()
    user = users[0]
    # Create API keys with specific names
    api_key1 = await user_api_key_factory.create(user=user, name="Test Key 1")
    await user_api_key_factory.create(user=user, name="Test Key 2")

    # Filter by name
    response = await auth_client.get(
        "/user-api-keys", params={"name__icontains": "Test Key 1"}
    )
    assert response.status_code == 200
    response_json = response.json()
    data = response_json["data"]
    assert len(data) == 1
    assert decode_id(data[0]["id"]) == api_key1.id
