from app.models.organization_wallet import OrganizationWallet
from tests.factories.async_factory import AsyncSQLAlchemyModelFactory
import factory
from tests.factories.organization_factory import OrganizationFactory
import pytest_asyncio


class OrganizationWalletFactory(AsyncSQLAlchemyModelFactory):
    class Meta:
        model = OrganizationWallet

    organization = factory.SubFactory(OrganizationFactory)
    stripe_customer_id = factory.Faker("uuid4")
    balance = 0


@pytest_asyncio.fixture
async def organization_wallet_factory(async_session):
    OrganizationWalletFactory._meta.session = async_session
    return OrganizationWalletFactory
