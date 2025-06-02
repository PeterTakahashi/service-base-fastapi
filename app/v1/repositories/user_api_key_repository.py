from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user_api_key import UserApiKey
from app.v1.repositories.base_repository import BaseRepository
from datetime import datetime


class UserApiKeyRepository(BaseRepository):
    default_scope = {"deleted_at__exact": None}

    def __init__(self, session: AsyncSession):
        super().__init__(session, UserApiKey)

    def soft_delete(self, id: int):
        """
        Soft delete a UserApiKey by its ID.
        Args:
            id (int): The ID of the UserApiKey to soft delete.
        """
        return self.update(id=id, deleted_at=datetime.utcnow())
