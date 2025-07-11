from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user_api_key import UserApiKey
from fastapi_repository import BaseRepository
from datetime import datetime


class UserApiKeyRepository(BaseRepository):
    default_scope = {"deleted_at__exact": None}

    def __init__(self, session: AsyncSession):
        super().__init__(session, UserApiKey)

    def soft_delete(self, id: int):
        return self.update(id=id, deleted_at=datetime.utcnow())
