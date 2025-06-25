import pytest_asyncio
from app.v1.services.organization_wallet_transaction_service import (
    OrganizationWalletTransactionService,
)


@pytest_asyncio.fixture
async def organization_wallet_transaction_service(
    organization_wallet_transaction_repository,
):
    return OrganizationWalletTransactionService(
        organization_wallet_transaction_repository
    )
