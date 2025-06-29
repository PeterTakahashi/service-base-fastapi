from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user_address import UserAddress
from fastapi_repository import BaseRepository


class UserAddressRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, UserAddress)
