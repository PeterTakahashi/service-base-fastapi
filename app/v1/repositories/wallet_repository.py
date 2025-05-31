from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.wallet import Wallet
from app.v1.repositories.base_repository import BaseRepository
from uuid import UUID


class WalletRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Wallet)

    async def get_wallet_by_user_id(self, user_id: UUID) -> Wallet | None:
        result = await self.session.execute(
            select(Wallet).filter(Wallet.user_id == user_id)
        )
        return result.scalars().first()

    async def update_wallet(self, wallet: Wallet, balance: int) -> Wallet:
        wallet.balance = balance
        self.session.add(wallet)
        await self.session.commit()
        await self.session.refresh(wallet)
        return wallet
