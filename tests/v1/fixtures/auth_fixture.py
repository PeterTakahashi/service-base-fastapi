import pytest_asyncio
from httpx import AsyncClient

@pytest_asyncio.fixture
async def access_token(client: AsyncClient, faker) -> str:
    email = faker.unique.email()
    password = faker.password(length=12)

    # Register user
    await client.post(
        "/auth/register/register", json={"email": email, "password": password}
    )

    # Login
    response = await client.post(
        "/auth/jwt/login",
        data={"username": email, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    return response.json()["access_token"]
