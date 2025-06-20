from app.models.user_wallet_transaction import UserWalletTransaction
from tests.factories.async_factory import AsyncSQLAlchemyModelFactory
import factory
from tests.factories.user_wallet_factory import UserWalletFactory
import pytest_asyncio


class UserWalletTransactionFactory(AsyncSQLAlchemyModelFactory):
    class Meta:
        model = UserWalletTransaction

    user_wallet = factory.SubFactory(UserWalletFactory)
    amount = factory.Faker("random_int", min=100, max=10000)
    stripe_payment_intent_id = factory.Faker("uuid4")
    user_wallet_transaction_type = factory.Faker(
        "random_element", elements=["DEPOSIT", "SPEND"]
    )
    user_wallet_transaction_status = factory.Faker(
        "random_element", elements=["PENDING", "COMPLETED", "FAILED"]
    )
    created_at = factory.Faker("date_time_this_year")
    updated_at = factory.Faker("date_time_this_year")


@pytest_asyncio.fixture
async def user_wallet_transaction_factory(async_session):
    UserWalletTransactionFactory._meta.session = async_session
    return UserWalletTransactionFactory
