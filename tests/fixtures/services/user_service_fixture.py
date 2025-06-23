import pytest_asyncio
from app.v1.services.user_service import UserService


@pytest_asyncio.fixture
async def user_service(user_repository):
    return UserService(user_repository)
