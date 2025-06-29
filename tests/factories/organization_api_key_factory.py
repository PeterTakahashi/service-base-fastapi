from app.models.organization_api_key import OrganizationApiKey
from tests.factories.async_factory import AsyncSQLAlchemyModelFactory
import factory
import pytest_asyncio
import secrets

from app.models.organization_api_key import API_KEY_PREFIX


class OrganizationApiKeyFactory(AsyncSQLAlchemyModelFactory):
    class Meta:
        model = OrganizationApiKey

    name = factory.Faker("word")
    api_key = factory.Sequence(
        lambda n: API_KEY_PREFIX + secrets.token_urlsafe(32) + str(n)
    )
    organization_id = factory.Faker("uuid4")
    expires_at = factory.Faker("future_datetime", end_date="+1y")
    allowed_origin = factory.Faker("url")
    allowed_ip = factory.Faker("ipv4")


@pytest_asyncio.fixture
async def organization_api_key_factory(async_session):
    OrganizationApiKeyFactory._meta.session = async_session
    return OrganizationApiKeyFactory
