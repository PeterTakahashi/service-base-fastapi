import pytest_asyncio
from app.v1.repositories.oauth_account_repository import OauthAccountRepository


@pytest_asyncio.fixture
async def oauth_account_repository(async_session):
    return OauthAccountRepository(async_session)
