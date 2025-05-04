from httpx import AsyncClient
from tests.common.check_error_response import (
    check_unauthorized_response,
    check_not_found_response,
)


async def test_create_character_with_multiple_images(
    auth_client: AsyncClient, product_id: str, init_character_image_files: list
):
    """
    Test creating a character with multiple images uploaded at once.
    """
    data = {"name": "MultiImageCharacter"}

    response = await auth_client.post(
        f"/products/{product_id}/characters/",
        data=data,
        files=init_character_image_files,
    )
    # Close the files after the request
    for _, (filename, file_obj, mime_type) in init_character_image_files:
        file_obj.close()

    assert (
        response.status_code == 201
    ), f"Expected 201, got {response.status_code}. Response: {response.text}"
    resp_data = response.json()

    # Basic assertions
    assert resp_data["name"] == "MultiImageCharacter"
    assert "character_images" in resp_data
    # We uploaded two images
    assert len(resp_data["character_images"]) == 2
    # Both should have valid presigned URLs
    assert resp_data["character_images"][0]["image_url"] != ""
    assert resp_data["character_images"][1]["image_url"] != ""


async def test_create_character_with_no_images(
    auth_client: AsyncClient, product_id: str
):
    """
    Test creating a character without any images.
    """
    data = {"name": "NoImageCharacter"}

    response = await auth_client.post(
        f"/products/{product_id}/characters/",
        json=data,
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
                "source": {"parameter": "name"},
            },
            {
                "status": "422",
                "code": "validation_error",
                "title": "Validation Error",
                "detail": "Field required",
                "source": {"parameter": "character_image_files"},
            },
        ]
    }


async def test_create_character_product_not_found(
    auth_client: AsyncClient, fake_id: str
):
    """
    Test that trying to get a character from a non-existent product returns 404.
    """
    response = await auth_client.get(f"/products/{fake_id}/characters/{fake_id}")
    check_not_found_response(response, "Product", "product_id", fake_id)


async def test_create_character_unauthorized(client: AsyncClient, fake_id: str):
    """
    Test creating a character without authorization should return 401.
    """
    data = {"name": "UnauthorizedCharacter"}
    files = {
        "character_image_files": (
            "1.png",
            open("tests/files/character_image/1.png", "rb"),
            "image/png",
        )
    }
    response = await client.post(
        f"/products/{fake_id}/characters/",
        data=data,
        files=files,
    )
    # Close the file
    files["character_image_files"][1].close()

    check_unauthorized_response(response)

async def test_create_character_over_max_character_image_files(
    auth_client: AsyncClient, product_id: str, over_max_character_image_files: list
):
    """
    Test creating a character with more than the maximum allowed images.
    """
    data = {"name": "OverMaxImageCharacter"}
    response = await auth_client.post(
        f"/products/{product_id}/characters/",
        data=data,
        files=over_max_character_image_files,
    )
    # Close the files after the request
    for _, (filename, file_obj, mime_type) in over_max_character_image_files:
        file_obj.close()

    assert (
        response.status_code == 422
    ), f"Expected 422, got {response.status_code}. Response: {response.text}"
    resp_data = response.json()
    assert resp_data['detail'] == {
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