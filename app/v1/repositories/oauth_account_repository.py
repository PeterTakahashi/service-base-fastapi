from sqlalchemy.ext.asyncio import AsyncSession
from app.models.oauth_account import OAuthAccount
from fastapi_repository import BaseRepository


class OauthAccountRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, OAuthAccount)
