from sqlalchemy.ext.asyncio import AsyncSession
from app.models.organization_address import OrganizationAddress
from app.v1.repositories.base_repository import BaseRepository


class OrganizationAddressRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, OrganizationAddress)
