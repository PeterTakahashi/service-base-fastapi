import pytest_asyncio
from app.v1.repositories.user_repository import UserRepository
from app.v1.repositories.wallet_repository import WalletRepository
from app.v1.repositories.wallet_transaction_repository import (
    WalletTransactionRepository,
)


@pytest_asyncio.fixture
async def user_repository(async_session):
    return UserRepository(async_session)


@pytest_asyncio.fixture
async def wallet_repository(async_session):
    return WalletRepository(async_session)


@pytest_asyncio.fixture
async def wallet_transaction_repository(async_session):
    return WalletTransactionRepository(async_session)
