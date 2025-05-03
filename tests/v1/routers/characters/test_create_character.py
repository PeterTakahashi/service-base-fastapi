import os
from httpx import AsyncClient
from tests.v1.common.unauthorized_response import check_unauthorized_response

async def test_create_character_with_single_image(auth_client: AsyncClient, product_id: str):
    """
    Test creating a character with a single image upload.
    """
    # Prepare file & form data
    files = {
        # "character_image_files" must match the parameter name in the route function
        "character_image_files": ("1.png", open("tests/files/character_image/1.png", "rb"), "image/png")
    }
    data = {
        "name": "SingleImageCharacter"
    }

    response = await auth_client.post(
        f"/products/{product_id}/characters/",
        data=data,
        files=files,
    )
    # Close the file to avoid file descriptor leaks
    files["character_image_files"][1].close()

    assert response.status_code == 201, f"Expected 201, got {response.status_code}. Response: {response.text}"
    resp_data = response.json()

    # Basic assertions
    assert resp_data["name"] == "SingleImageCharacter"
    assert "character_images" in resp_data
    assert len(resp_data["character_images"]) == 1
    assert resp_data["character_images"][0]["image_url"] != ""


async def test_create_character_with_multiple_images(auth_client: AsyncClient, product_id: str):
    """
    Test creating a character with multiple images uploaded at once.
    """
    # For multiple file uploads, pass each file under the same form field name (`character_image_files`)
    files = [
        (
            "character_image_files",
            ("1.png", open("tests/files/character_image/1.png", "rb"), "image/png"),
        ),
        (
            "character_image_files",
            ("2.png", open("tests/files/character_image/2.png", "rb"), "image/png"),
        ),
    ]
    data = {
        "name": "MultiImageCharacter"
    }

    response = await auth_client.post(
        f"/products/{product_id}/characters/",
        data=data,
        files=files,
    )
    # Close the files after the request
    for _, (filename, file_obj, mime_type) in files:
        file_obj.close()

    assert response.status_code == 201, f"Expected 201, got {response.status_code}. Response: {response.text}"
    resp_data = response.json()

    # Basic assertions
    assert resp_data["name"] == "MultiImageCharacter"
    assert "character_images" in resp_data
    # We uploaded two images
    assert len(resp_data["character_images"]) == 2
    # Both should have valid presigned URLs
    assert resp_data["character_images"][0]["image_url"] != ""
    assert resp_data["character_images"][1]["image_url"] != ""

async def test_create_character_unauthorized(client: AsyncClient, fake_id: str):
    """
    Test creating a character without authorization should return 401.
    """
    data = {"name": "UnauthorizedCharacter"}
    files = {
        "character_image_files": ("1.png", open("tests/files/character_image/1.png", "rb"), "image/png")
    }
    response = await client.post(
        f"/products/{fake_id}/characters/",
        data=data,
        files=files,
    )
    # Close the file
    files["character_image_files"][1].close()

    check_unauthorized_response(response)
