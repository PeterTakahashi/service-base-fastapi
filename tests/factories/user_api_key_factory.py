from app.models.user_api_key import UserApiKey
from tests.factories.async_factory import AsyncSQLAlchemyModelFactory
import factory
import pytest_asyncio
import secrets


class UserApiKeyFactory(AsyncSQLAlchemyModelFactory):
    class Meta:
        model = UserApiKey

    name = factory.Faker("word")
    api_key = factory.Sequence(lambda n: secrets.token_urlsafe(32) + str(n))
    user_id = factory.Faker("uuid4")
    expires_at = factory.Faker("future_datetime", end_date="+1y")
    allowed_origin = factory.Faker("url")
    allowed_ip = factory.Faker("ipv4")


@pytest_asyncio.fixture
async def user_api_key_factory(async_session):
    UserApiKeyFactory._meta.session = async_session
    return UserApiKeyFactory
