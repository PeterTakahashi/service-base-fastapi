from app.models.user_address import UserAddress
from tests.factories.async_factory import AsyncSQLAlchemyModelFactory
import factory
import pytest_asyncio


class UserAddressFactory(AsyncSQLAlchemyModelFactory):
    class Meta:
        model = UserAddress

    line1 = factory.Faker("street_address")
    line2 = factory.Faker("secondary_address")
    city = factory.Faker("city")
    state = factory.Faker("state")
    postal_code = factory.Faker("postcode")
    country = "US"

@pytest_asyncio.fixture
async def user_address_factory(async_session):
    UserAddressFactory._meta.session = async_session
    return UserAddressFactory
