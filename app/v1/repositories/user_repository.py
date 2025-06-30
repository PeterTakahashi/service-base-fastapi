from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from fastapi_repository import BaseRepository


class UserRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, User)
