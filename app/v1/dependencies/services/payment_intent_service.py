from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_async_session
from app.v1.repositories.user_wallet_repository import UserWalletRepository
from app.v1.repositories.user_wallet_transaction_repository import (
    UserWalletTransactionRepository,
)
from app.v1.services.payment_intent_service import PaymentIntentService


def get_payment_intent_service(
    session: AsyncSession = Depends(get_async_session),
) -> PaymentIntentService:
    user_wallet_repository = UserWalletRepository(session)
    user_wallet_transaction_repository = UserWalletTransactionRepository(session)
    return PaymentIntentService(
        user_wallet_repository, user_wallet_transaction_repository
    )
