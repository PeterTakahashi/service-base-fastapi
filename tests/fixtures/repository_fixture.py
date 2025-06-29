import pytest_asyncio
from app.v1.repositories.user_repository import UserRepository
from app.v1.repositories.user_wallet_repository import UserWalletRepository
from app.v1.repositories.user_wallet_transaction_repository import (
    UserWalletTransactionRepository,
)
from app.v1.repositories.user_api_key_repository import UserApiKeyRepository


@pytest_asyncio.fixture
async def user_repository(async_session):
    return UserRepository(async_session)


@pytest_asyncio.fixture
async def user_wallet_repository(async_session):
    return UserWalletRepository(async_session)


@pytest_asyncio.fixture
async def user_wallet_transaction_repository(async_session):
    return UserWalletTransactionRepository(async_session)


@pytest_asyncio.fixture
async def user_api_key_repository(async_session):
    return UserApiKeyRepository(async_session)
