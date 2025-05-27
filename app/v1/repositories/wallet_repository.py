from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.wallet import Wallet
from app.v1.repositories.base_repository import BaseRepository
from fastapi_users_db_sqlalchemy.generics import GUID


class WalletRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Wallet)

    async def get_wallet_by_user_id(self, user_id: GUID) -> Wallet | None:
        result = await self.session.execute(
            select(Wallet).filter(Wallet.user_id == user_id)
        )
        return result.scalars().first()

    async def create_wallet(self, user_id: GUID, stripe_customer_id: str) -> Wallet:
        wallet = Wallet(user_id=user_id, stripe_customer_id=stripe_customer_id)
        self.session.add(wallet)
        await self.session.commit()
        await self.session.refresh(wallet)
        return wallet
