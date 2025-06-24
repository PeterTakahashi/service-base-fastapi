from app.v1.repositories.organization_wallet_transaction_repository import (
    OrganizationWalletTransactionRepository,
)
from app.db.session import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends


def get_organization_wallet_transaction_repository(
    session: AsyncSession = Depends(get_async_session),
) -> OrganizationWalletTransactionRepository:
    return OrganizationWalletTransactionRepository(session)
