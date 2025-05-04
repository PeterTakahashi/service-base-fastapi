import pytest_asyncio
from httpx import AsyncClient
from faker import Faker


@pytest_asyncio.fixture
async def product(auth_client: AsyncClient, faker: Faker) -> dict:
    title = faker.unique.sentence(nb_words=3)
    response = await auth_client.post(
        "/products/",
        json={"title": title},
    )
    return response.json()


@pytest_asyncio.fixture
async def product_id(product: dict) -> str:
    return product["id"]
