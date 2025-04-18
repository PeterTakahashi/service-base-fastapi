from httpx import AsyncClient
from faker import Faker

fake = Faker()

async def get_access_token(client: AsyncClient) -> tuple[str, str]:
    email = fake.unique.email()
    password = fake.password(length=12)

    # Register user
    await client.post("/auth/register/register", json={"email": email, "password": password})

    # Login
    response = await client.post(
        "/auth/jwt/login",
        data={"username": email, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    access_token = response.json()["access_token"]
    return access_token, email
