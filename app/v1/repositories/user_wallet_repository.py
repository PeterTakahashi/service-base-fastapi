from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user_wallet import UserWallet
from fastapi_repository import BaseRepository


class UserWalletRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, UserWallet)
