from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_async_session
from app.v1.repositories.user_wallet_repository import UserWalletRepository
from app.v1.repositories.user_wallet_transaction_repository import (
    UserWalletTransactionRepository,
)
from app.v1.services.user_payment_intent_service import UserPaymentIntentService
from app.v1.dependencies.repositories.user_wallet_repository import (
    get_user_wallet_repository,
)
from app.v1.dependencies.repositories.user_wallet_transaction_repository import (
    get_user_wallet_transaction_repository,
)
from app.v1.dependencies.repositories.user_address_repository import (
    get_user_address_repository,
)
from app.v1.repositories.user_address_repository import UserAddressRepository

def get_user_payment_intent_service(
    user_wallet_repository: UserWalletRepository = Depends(get_user_wallet_repository),
    user_wallet_transaction_repository: UserWalletTransactionRepository = Depends(
        get_user_wallet_transaction_repository
    ),
    user_address_repository: UserAddressRepository = Depends(get_user_address_repository),
) -> UserPaymentIntentService:
    return UserPaymentIntentService(
        user_wallet_repository,
        user_wallet_transaction_repository,
        user_address_repository
    )
