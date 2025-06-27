from sqlalchemy.ext.asyncio import AsyncSession
from app.models.organization_api_key import OrganizationApiKey
from fastapi_repository import BaseRepository
from datetime import datetime


class OrganizationApiKeyRepository(BaseRepository):
    default_scope = {"deleted_at__exact": None}

    def __init__(self, session: AsyncSession):
        super().__init__(session, OrganizationApiKey)

    def soft_delete(self, id: int):
        return self.update(id=id, deleted_at=datetime.utcnow())
