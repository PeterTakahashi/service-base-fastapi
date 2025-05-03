import pytest_asyncio
from httpx import AsyncClient
from faker import Faker
import os

@pytest_asyncio.fixture
async def character(auth_client: AsyncClient, product_id: str, faker: Faker) -> dict:
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
        "name": faker.name(),
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
    return response.json()
