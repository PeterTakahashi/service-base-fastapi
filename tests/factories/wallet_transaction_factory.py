from app.models.wallet_transaction import WalletTransaction
from tests.factories.async_factory import AsyncSQLAlchemyModelFactory
import factory
from tests.factories.wallet_factory import WalletFactory


class WalletTransactionFactory(AsyncSQLAlchemyModelFactory):
    class Meta:
        model = WalletTransaction

    wallet = factory.SubFactory(WalletFactory)
    amount = factory.Faker("random_int", min=100, max=10000)
    stripe_payment_intent_id = factory.Faker("uuid4")
    wallet_transaction_type = factory.Faker(
        "random_element", elements=["DEPOSIT", "WITHDRAWAL"]
    )
    wallet_transaction_status = factory.Faker(
        "random_element", elements=["PENDING", "COMPLETED", "FAILED"]
    )
    created_at = factory.Faker("date_time_this_year")
    updated_at = factory.Faker("date_time_this_year")
