from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_async_session
from app.v1.repositories.organization_wallet_repository import OrganizationWalletRepository
from app.v1.repositories.organization_wallet_transaction_repository import (
    OrganizationWalletTransactionRepository,
)
from app.v1.services.organization_payment_intent_service import OrganizationPaymentIntentService
from app.v1.dependencies.repositories.organization_wallet_repository import (
    get_organization_wallet_repository,
)
from app.v1.dependencies.repositories.organization_wallet_transaction_repository import (
    get_organization_wallet_transaction_repository,
)
from app.v1.dependencies.repositories.organization_address_repository import (
    get_organization_address_repository,
)
from app.v1.repositories.organization_address_repository import OrganizationAddressRepository

def get_organization_payment_intent_service(
    organization_wallet_repository: OrganizationWalletRepository = Depends(get_organization_wallet_repository),
    organization_wallet_transaction_repository: OrganizationWalletTransactionRepository = Depends(
        get_organization_wallet_transaction_repository
    ),
    organization_address_repository: OrganizationAddressRepository = Depends(get_organization_address_repository),
) -> OrganizationPaymentIntentService:
    return OrganizationPaymentIntentService(
        organization_wallet_repository,
        organization_wallet_transaction_repository,
        organization_address_repository
    )
