import pytest_asyncio
from httpx import AsyncClient
from faker import Faker

@pytest_asyncio.fixture
async def init_character_image_files():
    """
    Fixture to provide a list of file tuples for testing.
    """
    return [
        (
            "character_image_files",
            ("1.png", open("tests/files/character_image/1.png", "rb"), "image/png"),
        ),
        (
            "character_image_files",
            ("2.png", open("tests/files/character_image/2.png", "rb"), "image/png"),
        ),
    ]

@pytest_asyncio.fixture
async def over_max_character_image_files():
    """
    Fixture to provide a list of file tuples for testing.
    """
    files = []
    for i in range(1, 12):
        files.append(
            (
                "character_image_files",
                (f"{i}.png", open(f"tests/files/character_image/{i}.png", "rb"), "image/png"),
            )
        )
    return files

@pytest_asyncio.fixture
async def character(auth_client: AsyncClient, product_id: str, faker: Faker, init_character_image_files) -> dict:
    data = {
        "name": faker.name(),
    }

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
    return response.json()

@pytest_asyncio.fixture
async def character_id(character: dict) -> str:
    """
    Fixture to extract and return the character ID from the character fixture.
    """
    return character["id"]