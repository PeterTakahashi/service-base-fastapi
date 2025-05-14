from httpx import AsyncClient
from tests.common.check_error_response import (
    check_unauthorized_response,
    check_not_found_response,
)


async def test_delete_character_image(
    auth_client: AsyncClient,
    product_id: str,
    character_id: str,
    character_image_id: str,
):
    """
    Test deleting a character image.
    """
    response = await auth_client.delete(
        f"/products/{product_id}/characters/{character_id}/character-images/{character_image_id}"
    )

    assert (
        response.status_code == 204
    ), f"Expected 204, got {response.status_code}. Response: {response.text}"
    assert response.text == ""


async def test_delete_character_image_product_not_found(
    auth_client: AsyncClient, fake_id: str, character_id: str, character_image_id: str
):
    response = await auth_client.delete(
        f"/products/{fake_id}/characters/{character_id}/character-images/{character_image_id}"
    )
    check_not_found_response(response, "Product", "product_id", fake_id)


async def test_delete_character_image_character_not_found(
    auth_client: AsyncClient, fake_id: str, product_id: str, character_image_id: str
):
    response = await auth_client.delete(
        f"/products/{product_id}/characters/{fake_id}/character-images/{character_image_id}"
    )
    check_not_found_response(response, "Character", "character_id", fake_id)


async def test_delete_character_image_not_found(
    auth_client: AsyncClient, product_id: str, character_id: str, fake_id: str
):
    response = await auth_client.delete(
        f"/products/{product_id}/characters/{character_id}/character-images/{fake_id}"
    )
    check_not_found_response(response, "CharacterImage", "character_image_id", fake_id)


async def test_delete_character_image_unauthorized(client: AsyncClient, fake_id: str):
    response = await client.delete(
        f"/products/{fake_id}/characters/{fake_id}/character-images/{fake_id}"
    )
    check_unauthorized_response(response)
