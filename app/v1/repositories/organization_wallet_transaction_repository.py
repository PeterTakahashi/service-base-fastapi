from sqlalchemy.ext.asyncio import AsyncSession
from app.models.organization_wallet_transaction import OrganizationWalletTransaction
from app.v1.repositories.base_repository import BaseRepository


class OrganizationWalletTransactionRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, OrganizationWalletTransaction)
