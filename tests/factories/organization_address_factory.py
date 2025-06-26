from app.models.organization_address import OrganizationAddress
from tests.factories.async_factory import AsyncSQLAlchemyModelFactory
import factory
import pytest_asyncio


class OrganizationAddressFactory(AsyncSQLAlchemyModelFactory):
    class Meta:
        model = OrganizationAddress

    line1 = factory.Faker("street_address")
    line2 = factory.Faker("secondary_address")
    city = factory.Faker("city")
    state = factory.Faker("state")
    postal_code = factory.Faker("postcode")
    country = "US"


@pytest_asyncio.fixture
async def organization_address_factory(async_session):
    OrganizationAddressFactory._meta.session = async_session
    return OrganizationAddressFactory
