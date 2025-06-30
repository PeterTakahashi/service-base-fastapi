from app.v1.repositories.organization_api_key_repository import (
    OrganizationApiKeyRepository,
)
from app.db.session import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends


def get_organization_api_key_repository(
    session: AsyncSession = Depends(get_async_session),
) -> OrganizationApiKeyRepository:
    return OrganizationApiKeyRepository(session)
