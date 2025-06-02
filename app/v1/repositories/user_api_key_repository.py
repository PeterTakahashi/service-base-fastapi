from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user_api_key import UserApiKey
from app.v1.repositories.base_repository import BaseRepository


class UserApiKeyRepository(BaseRepository):
    default_scope = {"deleted_at__exact": None}

    def __init__(self, session: AsyncSession):
        super().__init__(session, UserApiKey)
