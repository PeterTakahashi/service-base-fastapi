from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user_wallet_transaction import (
    UserWalletTransaction,
)
from fastapi_repository import BaseRepository


class UserWalletTransactionRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, UserWalletTransaction)
