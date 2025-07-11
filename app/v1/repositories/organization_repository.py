from sqlalchemy.ext.asyncio import AsyncSession
from app.models.organization import Organization
from fastapi_repository import BaseRepository
from datetime import datetime


class OrganizationRepository(BaseRepository):
    default_scope = {"deleted_at__exact": None}

    def __init__(self, session: AsyncSession):
        super().__init__(session, Organization)

    def soft_delete(self, id: int):
        return self.update(id=id, deleted_at=datetime.utcnow())
