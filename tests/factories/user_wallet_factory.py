from app.models.user_wallet import UserWallet
from tests.factories.async_factory import AsyncSQLAlchemyModelFactory
import factory
from tests.factories.user_factory import UserFactory
import pytest_asyncio


class UserWalletFactory(AsyncSQLAlchemyModelFactory):
    class Meta:
        model = UserWallet

    user = factory.SubFactory(UserFactory)
    stripe_customer_id = factory.Faker("uuid4")
    balance = 0


@pytest_asyncio.fixture
async def user_wallet_factory(async_session):
    UserWalletFactory._meta.session = async_session
    return UserWalletFactory
