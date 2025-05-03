import pytest_asyncio
from httpx import AsyncClient
from faker import Faker

@pytest_asyncio.fixture
async def character(auth_client: AsyncClient, faker: Faker) -> dict:
    name = faker.unique.sentence(nb_words=3)
    response = await auth_client.post(
        "/characters/",
        json={"name": name},
    )
    return response.json()