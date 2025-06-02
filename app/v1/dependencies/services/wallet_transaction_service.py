from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_async_session

from app.v1.repositories.wallet_transaction_repository import (
    WalletTransactionRepository,
)
from app.v1.services.wallet_transaction_service import WalletTransactionService


def get_wallet_transaction_service(
    session: AsyncSession = Depends(get_async_session),
) -> WalletTransactionService:
    wallet_transaction_repository = WalletTransactionRepository(session)
    return WalletTransactionService(wallet_transaction_repository)
