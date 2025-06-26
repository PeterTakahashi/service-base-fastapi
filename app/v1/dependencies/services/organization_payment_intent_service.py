from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_async_session
from app.v1.repositories.organization_wallet_repository import (
    OrganizationWalletRepository,
)
from app.v1.repositories.organization_wallet_transaction_repository import (
    OrganizationWalletTransactionRepository,
)
from app.v1.services.organization_payment_intent_service import (
    OrganizationPaymentIntentService,
)


def get_organization_payment_intent_service(
    session: AsyncSession = Depends(get_async_session),
) -> OrganizationPaymentIntentService:
    organization_wallet_repository = OrganizationWalletRepository(session)
    organization_wallet_transaction_repository = (
        OrganizationWalletTransactionRepository(session)
    )
    return OrganizationPaymentIntentService(
        organization_wallet_repository, organization_wallet_transaction_repository
    )
