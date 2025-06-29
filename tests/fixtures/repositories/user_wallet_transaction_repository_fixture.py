import pytest_asyncio
from app.v1.repositories.user_wallet_transaction_repository import (
    UserWalletTransactionRepository,
)


@pytest_asyncio.fixture
async def user_wallet_transaction_repository(async_session):
    return UserWalletTransactionRepository(async_session)
