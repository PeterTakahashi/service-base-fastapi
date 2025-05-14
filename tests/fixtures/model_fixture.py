import pytest_asyncio
from tests.factories.user_factory import UserFactory


@pytest_asyncio.fixture
async def user(async_session):
    UserFactory._meta.session = async_session
    user = await UserFactory.create()
    return user
