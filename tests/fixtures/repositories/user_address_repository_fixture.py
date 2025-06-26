import pytest_asyncio
from app.v1.repositories.user_address_repository import UserAddressRepository


@pytest_asyncio.fixture
async def user_address_repository(async_session):
    return UserAddressRepository(async_session)
