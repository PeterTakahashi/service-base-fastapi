from fastapi import Depends
from app.v1.repositories.user_wallet_repository import UserWalletRepository
from app.v1.repositories.user_wallet_transaction_repository import (
    UserWalletTransactionRepository,
)
from app.v1.repositories.organization_wallet_repository import (
    OrganizationWalletRepository,
)
from app.v1.repositories.organization_wallet_transaction_repository import (
    OrganizationWalletTransactionRepository,
)
from app.v1.dependencies.repositories.user_wallet_transaction_repository import (
    get_user_wallet_transaction_repository,
)
from app.v1.dependencies.repositories.user_wallet_repository import (
    get_user_wallet_repository,
)
from app.v1.dependencies.repositories.organization_wallet_repository import (
    get_organization_wallet_repository,
)
from app.v1.dependencies.repositories.organization_wallet_transaction_repository import (
    get_organization_wallet_transaction_repository,
)

from app.v1.services.payment_intent_service import PaymentIntentService


def get_payment_intent_service(
    user_wallet_repository: UserWalletRepository = Depends(get_user_wallet_repository),
    user_wallet_transaction_repository: UserWalletTransactionRepository = Depends(
        get_user_wallet_transaction_repository
    ),
    organization_wallet_repository: OrganizationWalletRepository = Depends(
        get_organization_wallet_repository
    ),
    organization_wallet_transaction_repository: OrganizationWalletTransactionRepository = Depends(
        get_organization_wallet_transaction_repository
    ),
) -> PaymentIntentService:
    return PaymentIntentService(
        user_wallet_repository,
        user_wallet_transaction_repository,
        organization_wallet_repository,
        organization_wallet_transaction_repository,
    )
