from app.v1.repositories.organization_address_repository import (
    OrganizationAddressRepository,
)
from app.db.session import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends


def get_organization_address_repository(
    session: AsyncSession = Depends(get_async_session),
) -> OrganizationAddressRepository:
    return OrganizationAddressRepository(session)
