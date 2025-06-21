from sqlalchemy.ext.asyncio import AsyncSession
from app.models.organization import Organization
from app.v1.repositories.base_repository import BaseRepository
from datetime import datetime


class OrganizationRepository(BaseRepository):
    default_scope = {"deleted_at__exact": None}

    def __init__(self, session: AsyncSession):
        super().__init__(session, Organization)

    def soft_delete(self, id: int):
        """
        Soft delete an Organization by its ID.
        Args:
            id (int): The ID of the Organization to soft delete.
        """
        return self.update(id=id, deleted_at=datetime.utcnow())
