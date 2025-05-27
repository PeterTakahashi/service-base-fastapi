from sqlalchemy.ext.asyncio import AsyncSession
from app.models.wallet_transaction import (
    WalletTransaction,
    WalletTransactionStatus,
    WalletTransactionType,
)
from app.v1.repositories.base_repository import BaseRepository
from sqlalchemy.future import select
from typing import Optional


class WalletTransactionRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, WalletTransaction)

    async def get_latest_wallet_transaction_by_wallet_id(
        self, wallet_id: int
    ) -> WalletTransaction | None:
        result = await self.session.execute(
            select(WalletTransaction)
            .filter(WalletTransaction.wallet_id == wallet_id)
            .order_by(WalletTransaction.created_at.desc())
            .limit(1)
        )
        return result.scalars().first()

    async def create_wallet_transaction(
        self,
        wallet_id: int,
        amount: int,
        stripe_payment_intent_id: Optional[str] = None,
        wallet_transaction_type: WalletTransactionType = WalletTransactionType.DEPOSIT,
        wallet_transaction_status: WalletTransactionStatus = WalletTransactionStatus.PENDING,
    ) -> WalletTransaction:
        wallet_transaction = WalletTransaction(
            wallet_id=wallet_id,
            amount=amount,
            stripe_payment_intent_id=stripe_payment_intent_id,
            wallet_transaction_type=wallet_transaction_type,
            wallet_transaction_status=wallet_transaction_status,
        )
        self.session.add(wallet_transaction)
        await self.session.commit()
        await self.session.refresh(wallet_transaction)
        return wallet_transaction
