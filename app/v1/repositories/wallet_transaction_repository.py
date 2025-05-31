from sqlalchemy.ext.asyncio import AsyncSession
from app.models.wallet_transaction import (
    WalletTransaction,
)
from app.v1.repositories.base_repository import BaseRepository


class WalletTransactionRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, WalletTransaction)
