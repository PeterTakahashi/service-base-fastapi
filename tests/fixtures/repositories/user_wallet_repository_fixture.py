import pytest_asyncio
from app.v1.repositories.user_wallet_repository import UserWalletRepository


@pytest_asyncio.fixture
async def user_wallet_repository(async_session):
    return UserWalletRepository(async_session)
