from app.models.wallet import Wallet
from tests.factories.async_factory import AsyncSQLAlchemyModelFactory
import factory
from tests.factories.user_factory import UserFactory
import pytest_asyncio


class WalletFactory(AsyncSQLAlchemyModelFactory):
    class Meta:
        model = Wallet

    user = factory.SubFactory(UserFactory)
    stripe_customer_id = factory.Faker("uuid4")
    balance = 1000


@pytest_asyncio.fixture
async def wallet_factory(async_session):
    WalletFactory._meta.session = async_session
    return WalletFactory
