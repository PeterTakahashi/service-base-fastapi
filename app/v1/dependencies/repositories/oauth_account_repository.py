from app.v1.repositories.oauth_account_repository import OauthAccountRepository
from app.db.session import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends


def get_oauth_account_repository(
    session: AsyncSession = Depends(get_async_session),
) -> OauthAccountRepository:
    return OauthAccountRepository(session)
