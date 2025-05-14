import pytest_asyncio
from httpx import AsyncClient


@pytest_asyncio.fixture
async def character_image_id(
    auth_client: AsyncClient, product_id: str, character_id: str
) -> str:
    """
    Fixture to provide a character image ID for testing.
    """
    response = await auth_client.get(
        f"/products/{product_id}/characters/{character_id}",
    )
    return response.json()["character_images"][0]["id"]
