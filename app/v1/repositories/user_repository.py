from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.v1.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, User)
