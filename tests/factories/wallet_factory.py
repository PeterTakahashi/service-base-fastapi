from app.models.wallet import Wallet
from tests.factories.async_factory import AsyncSQLAlchemyModelFactory
import factory
from tests.factories.user_factory import UserFactory


class WalletFactory(AsyncSQLAlchemyModelFactory):
    class Meta:
        model = Wallet

    user = factory.SubFactory(UserFactory)
    stripe_customer_id = factory.Faker("uuid4")
    balance = 1000
