from app.v1.repositories.organization_wallet_repository import (
    OrganizationWalletRepository,
)
from app.db.session import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends


def get_organization_wallet_repository(
    session: AsyncSession = Depends(get_async_session),
) -> OrganizationWalletRepository:
    return OrganizationWalletRepository(session)
