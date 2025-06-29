from fastapi import Depends

from app.v1.repositories.organization_wallet_transaction_repository import (
    OrganizationWalletTransactionRepository,
)
from app.v1.services.organization_wallet_transaction_service import (
    OrganizationWalletTransactionService,
)
from app.v1.dependencies.repositories.organization_wallet_transaction_repository import (
    get_organization_wallet_transaction_repository,
)


def get_organization_wallet_transaction_service(
    organization_wallet_transaction_repository: OrganizationWalletTransactionRepository = Depends(
        get_organization_wallet_transaction_repository
    ),
) -> OrganizationWalletTransactionService:
    return OrganizationWalletTransactionService(
        organization_wallet_transaction_repository
    )
