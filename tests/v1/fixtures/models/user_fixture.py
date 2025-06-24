import pytest_asyncio

from httpx import AsyncClient
from app.models.user import User


@pytest_asyncio.fixture
async def user(auth_client: AsyncClient, user_repository) -> User:
    response = await auth_client.get("/users/me")
    response_data = response.json()
    user = await user_repository.find_by(email=response_data["email"])
    return user


@pytest_asyncio.fixture
async def other_user(other_auth_client: AsyncClient, user_repository) -> User:
    response = await other_auth_client.get("/users/me")
    response_data = response.json()
    user = await user_repository.find_by(email=response_data["email"])
    return user
