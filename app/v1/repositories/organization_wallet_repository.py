from sqlalchemy.ext.asyncio import AsyncSession
from app.models.organization_wallet import OrganizationWallet
from fastapi_repository import BaseRepository


class OrganizationWalletRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, OrganizationWallet)
