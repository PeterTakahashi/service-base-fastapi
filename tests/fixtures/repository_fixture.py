import pytest_asyncio
from app.v1.repositories.user_repository import UserRepository


@pytest_asyncio.fixture
async def user_repository(async_session):
    return UserRepository(async_session)
