from httpx import AsyncClient
from tests.common.check_error_response import (
    check_unauthorized_response,
    check_not_found_response,
)


async def test_delete_character_image(
    auth_client: AsyncClient,
    character_image_id: str,
):
    """
    Test deleting a character image.
    """
    response = await auth_client.delete(f"/character-images/{character_image_id}")

    assert (
        response.status_code == 204
    ), f"Expected 204, got {response.status_code}. Response: {response.text}"
    assert response.text == ""


async def test_delete_character_image_not_found(auth_client: AsyncClient, fake_id: str):
    response = await auth_client.delete(f"/character-images/{fake_id}")
    check_not_found_response(response, "CharacterImage", "character_image_id", fake_id)


async def test_delete_character_image_unauthorized(client: AsyncClient, fake_id: str):
    response = await client.delete(f"/character-images/{fake_id}")
    check_unauthorized_response(response)
