from httpx import AsyncClient
import pytest_asyncio
from tests.common.check_error_response import (
    check_unauthorized_response,
    check_not_found_response,
)


@pytest_asyncio.fixture
async def character_image_files():
    """
    Fixture to provide a list of file tuples for testing.
    """
    return [
        (
            "character_image_files",
            ("3.png", open("tests/files/character_image/3.png", "rb"), "image/png"),
        ),
        (
            "character_image_files",
            ("4.png", open("tests/files/character_image/4.png", "rb"), "image/png"),
        ),
    ]


async def test_add_character_images_character(
    auth_client: AsyncClient, product_id: str, character_id: str, character_image_files
):
    """
    Test adding images to a character.
    """
    response = await auth_client.put(
        f"/products/{product_id}/characters/{character_id}/add-character-images",
        data={},
        files=character_image_files,
    )
    # Close the files to avoid file descriptor leaks
    for _, file in character_image_files:
        file[1].close()

    assert (
        response.status_code == 200
    ), f"Expected 200, got {response.status_code}. Response: {response.text}"
    resp_data = response.json()

    # Basic assertions
    assert resp_data["id"] == character_id
    assert resp_data["product_id"] == product_id
    assert resp_data["name"] != ""
    assert "character_images" in resp_data
    assert len(resp_data["character_images"]) == 4


async def test_add_character_images_with_no_images(
    auth_client: AsyncClient, product_id: str, character_id: str
):
    """
    Test creating a character without any images.
    """
    response = await auth_client.put(
        f"/products/{product_id}/characters/{character_id}/add-character-images",
        data={},
        files=[],
    )
    assert (
        response.status_code == 422
    ), f"Expected 422, got {response.status_code}. Response: {response.text}"
    resp_data = response.json()
    assert resp_data == {
        "errors": [
            {
                "status": "422",
                "code": "validation_error",
                "title": "Validation Error",
                "detail": "Field required",
                "source": {"parameter": "character_image_files"},
            },
        ]
    }


async def test_add_character_images_unauthorized(client: AsyncClient, fake_id: str):
    """
    Test adding images to a character without authorization should return 401.
    """
    response = await client.put(
        f"/products/{fake_id}/characters/{fake_id}/add-character-images",
        data={},
        files=[],
    )

    check_unauthorized_response(response)


async def test_add_character_images_not_found_product(
    auth_client: AsyncClient, fake_id: str, character_image_files
):
    """
    Test adding images to a character with a non-existent product should return 404.
    """
    response = await auth_client.put(
        f"/products/{fake_id}/characters/{fake_id}/add-character-images",
        data={},
        files=character_image_files,
    )
    # Close the files to avoid file descriptor leaks
    for _, file in character_image_files:
        file[1].close()
    check_not_found_response(response, "Product", "product_id", fake_id)


async def test_add_character_images_not_found_character(
    auth_client: AsyncClient, product_id: str, fake_id: str, character_image_files
):
    """
    Test adding images to a non-existent character should return 404.
    """
    response = await auth_client.put(
        f"/products/{product_id}/characters/{fake_id}/add-character-images",
        data={},
        files=character_image_files,
    )
    # Close the files to avoid file descriptor leaks
    for _, file in character_image_files:
        file[1].close()
    check_not_found_response(response, "Character", "character_id", fake_id)


async def test_add_character_images_over_max_images(
    auth_client: AsyncClient,
    product_id: str,
    character_id: str,
    over_max_character_image_files: list,
):
    """
    Test adding more than the maximum allowed images to a character.
    """
    response = await auth_client.put(
        f"/products/{product_id}/characters/{character_id}/add-character-images",
        data={},
        files=over_max_character_image_files,
    )
    # Close the files to avoid file descriptor leaks
    for _, file in over_max_character_image_files:
        file[1].close()

    assert (
        response.status_code == 422
    ), f"Expected 422, got {response.status_code}. Response: {response.text}"
    resp_data = response.json()
    assert resp_data["detail"] == {
        "errors": [
            {
                "status": "422",
                "code": "invalid_request",
                "title": "Unprocessable Entity",
                "detail": "Character image count must be between 1 and 10.",
                "source": {"parameter": "character_image_files"},
            }
        ]
    }
