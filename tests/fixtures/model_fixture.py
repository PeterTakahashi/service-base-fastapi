import pytest_asyncio
from tests.factories.user_factory import UserFactory
from tests.factories.wallet_factory import WalletFactory

@pytest_asyncio.fixture
async def user(async_session):
    UserFactory._meta.session = async_session
    user = await UserFactory.create()
    return user

@pytest_asyncio.fixture
async def wallet(async_session, user):
    WalletFactory._meta.session = async_session
    wallet = await WalletFactory.create(user=user)
    return wallet