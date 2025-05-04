from httpx import AsyncClient
from faker import Faker

fake = Faker()


async def create_product(auth_client: AsyncClient, title: str | None = None) -> dict:
    if title is None:
        title = fake.unique.sentence(nb_words=3)

    response = await auth_client.post(
        "/products/",
        json={"title": title},
    )
    assert response.status_code == 201
    return response.json()
