import pytest_asyncio
from httpx import AsyncClient
from faker import Faker
from app.v1.repositories.user_repository import UserRepository


@pytest_asyncio.fixture
async def not_verified_access_token(
    client: AsyncClient, faker: Faker, fake_email: str
) -> str:
    email = fake_email
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


@pytest_asyncio.fixture
async def access_token(
    client: AsyncClient,
    not_verified_access_token: str,
    user_repository: UserRepository,
    fake_email: str,
) -> str:
    user = await user_repository.find_by(email=fake_email)
    await user_repository.update(id=user.id, is_verified=True)
    return not_verified_access_token


@pytest_asyncio.fixture
async def authed_user(
    access_token: str,
    user_repository: UserRepository,
    fake_email: str,
):
    user = await user_repository.find_by(email=fake_email)
    return user
