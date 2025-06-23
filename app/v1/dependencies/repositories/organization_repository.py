from app.v1.repositories.organization_repository import OrganizationRepository
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_async_session


def get_organization_repository(
    session: AsyncSession = Depends(get_async_session),
) -> OrganizationRepository:
    return OrganizationRepository(session)
