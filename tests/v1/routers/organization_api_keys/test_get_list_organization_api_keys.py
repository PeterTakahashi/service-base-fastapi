import pytest

from httpx import AsyncClient
from app.lib.utils.convert_id import decode_id, encode_id


@pytest.mark.asyncio
async def test_list_organization_api_keys_no_filter(
    auth_client: AsyncClient,
    organization_api_key_factory,
    organization,
    user,
):
    """
    Test that all organization API keys for the authenticated organization are returned when no filter is provided.
    """
    # Create multiple API keys for the same organization
    api_key1 = await organization_api_key_factory.create(
        organization=organization, created_by_user=user
    )
    api_key2 = await organization_api_key_factory.create(
        organization=organization, created_by_user=user
    )

    response = await auth_client.get(
        f"/organizations/{encode_id(organization.id)}/api-keys"
    )
    assert response.status_code == 200

    response_json = response.json()
    data = response_json["data"]

    # We expect only api_key1 and api_key2
    returned_ids = sorted(decode_id(api_key["id"]) for api_key in data)
    expected_ids = sorted([api_key1.id, api_key2.id])

    assert returned_ids == expected_ids


@pytest.mark.asyncio
async def test_list_organization_api_keys_with_filter(
    auth_client: AsyncClient,
    organization_api_key_factory,
    organization,
    user,
):
    """
    Test that organization API keys can be filtered by name and api_key.
    """
    # Create API keys with specific names
    api_key1 = await organization_api_key_factory.create(
        organization=organization, name="Test Key 1", created_by_user=user
    )
    await organization_api_key_factory.create(
        organization=organization, name="Test Key 2", created_by_user=user
    )

    # Filter by name
    response = await auth_client.get(
        f"/organizations/{encode_id(organization.id)}/api-keys",
        params={"name__icontains": "Test Key 1"},
    )
    assert response.status_code == 200
    response_json = response.json()
    data = response_json["data"]
    assert len(data) == 1
    assert decode_id(data[0]["id"]) == api_key1.id
