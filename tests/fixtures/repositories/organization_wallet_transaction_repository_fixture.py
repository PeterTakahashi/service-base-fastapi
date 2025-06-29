import pytest_asyncio
from app.v1.repositories.organization_wallet_transaction_repository import (
    OrganizationWalletTransactionRepository,
)


@pytest_asyncio.fixture
async def organization_wallet_transaction_repository(async_session):
    return OrganizationWalletTransactionRepository(async_session)
