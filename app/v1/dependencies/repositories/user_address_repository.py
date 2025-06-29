from app.v1.repositories.user_address_repository import UserAddressRepository
from app.db.session import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends


def get_user_address_repository(
    session: AsyncSession = Depends(get_async_session),
) -> UserAddressRepository:
    return UserAddressRepository(session)
