import pytest_asyncio
from app.v1.repositories.organization_wallet_repository import OrganizationWalletRepository


@pytest_asyncio.fixture
async def organization_wallet_repository(async_session):
    return OrganizationWalletRepository(async_session)
