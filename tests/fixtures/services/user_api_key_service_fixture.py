import pytest_asyncio
from app.v1.services.user_api_key_service import UserApiKeyService


@pytest_asyncio.fixture
async def user_api_key_service(user_api_key_repository):
    return UserApiKeyService(user_api_key_repository)
