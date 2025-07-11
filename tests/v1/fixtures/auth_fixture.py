import pytest_asyncio
from httpx import AsyncClient
from faker import Faker
from app.v1.repositories.user_repository import UserRepository


async def create_and_get_access_token(
    client: AsyncClient, email: str, password: str
) -> str:
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
async def not_verified_access_token(
    client: AsyncClient, faker: Faker, fake_email: str
) -> str:
    return await create_and_get_access_token(
        client, fake_email, faker.password(length=12)
    )


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
async def other_access_token(
    client: AsyncClient,
    faker: Faker,
    user_repository: UserRepository,
) -> str:
    email = faker.email()
    password = faker.password(length=12)
    access_token = await create_and_get_access_token(client, email, password)
    user = await user_repository.find_by(email=email)
    await user_repository.update(id=user.id, is_verified=True)
    return access_token
