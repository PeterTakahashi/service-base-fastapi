import pytest
from httpx import AsyncClient
from tests.v1.common.unauthorized_response import check_unauthorized_response

async def test_get_character_success(auth_client: AsyncClient, product_id: str, character: dict):
    character_id = character["id"]
    response = await auth_client.get(f"/products/{product_id}/characters/{character_id}")
    assert response.status_code == 200
    fetched_character = response.json()

    assert fetched_character["id"] == character_id
    assert fetched_character["name"] == character["name"]
    assert "character_images" in fetched_character
    assert len(fetched_character["character_images"]) == 2

async def test_get_character_not_found(auth_client: AsyncClient, product_id: str, fake_id: str):
    """
    Test that trying to get a non-existent character returns 404.
    """
    resp = await auth_client.get(f"/products/{product_id}/characters/{fake_id}")
    assert resp.status_code == 404
    body = resp.json()
    assert body["detail"]["errors"][0]["code"] == "character_not_found"
    assert "Not Found" in body["detail"]["errors"][0]["title"]


async def test_get_character_unauthorized(client: AsyncClient, fake_id: str):
    """
    Test that attempting to retrieve a character without authorization returns 401.
    """
    response = await client.get(f"/products/{fake_id}/characters/{fake_id}")
    check_unauthorized_response(response)
