from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_async_session

from app.v1.repositories.organization_wallet_transaction_repository import (
    OrganizationWalletTransactionRepository,
)
from app.v1.services.organization_wallet_transaction_service import (
    OrganizationWalletTransactionService,
)


def get_organization_wallet_transaction_service(
    session: AsyncSession = Depends(get_async_session),
) -> OrganizationWalletTransactionService:
    organization_wallet_transaction_repository = (
        OrganizationWalletTransactionRepository(session)
    )
    return OrganizationWalletTransactionService(
        organization_wallet_transaction_repository
    )
