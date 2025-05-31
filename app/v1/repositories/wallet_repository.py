from sqlalchemy.ext.asyncio import AsyncSession
from app.models.wallet import Wallet
from app.v1.repositories.base_repository import BaseRepository


class WalletRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Wallet)

    async def update_wallet(self, wallet: Wallet, balance: int) -> Wallet:
        wallet.balance = balance
        self.session.add(wallet)
        await self.session.commit()
        await self.session.refresh(wallet)
        return wallet
