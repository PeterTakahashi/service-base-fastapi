import pytest_asyncio
from app.v1.repositories.user_api_key_repository import UserApiKeyRepository


@pytest_asyncio.fixture
async def user_api_key_repository(async_session):
    return UserApiKeyRepository(async_session)
