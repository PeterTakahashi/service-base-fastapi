from httpx import AsyncClient
from faker import Faker

fake = Faker()

async def create_product(
    client: AsyncClient, token: str, title: str | None = None
) -> dict:
    if title is None:
        title = fake.unique.sentence(nb_words=3)

    response = await client.post(
        "/products/",
        json={"title": title},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201
    return response.json()
