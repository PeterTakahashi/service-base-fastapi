from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_async_session
from app.v1.repositories.wallet_repository import WalletRepository
from app.v1.repositories.wallet_transaction_repository import (
    WalletTransactionRepository,
)
from app.v1.services.payment_intent_service import PaymentIntentService


def get_payment_intent_service(
    session: AsyncSession = Depends(get_async_session),
) -> PaymentIntentService:
    wallet_repository = WalletRepository(session)
    wallet_transaction_repository = WalletTransactionRepository(session)
    return PaymentIntentService(wallet_repository, wallet_transaction_repository)
