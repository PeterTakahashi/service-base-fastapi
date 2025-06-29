from app.models.organization_wallet_transaction import OrganizationWalletTransaction
from tests.factories.async_factory import AsyncSQLAlchemyModelFactory
import factory
from tests.factories.organization_wallet_factory import OrganizationWalletFactory
import pytest_asyncio


class OrganizationWalletTransactionFactory(AsyncSQLAlchemyModelFactory):
    class Meta:
        model = OrganizationWalletTransaction

    organization_wallet = factory.SubFactory(OrganizationWalletFactory)
    amount = factory.Faker("random_int", min=100, max=10000)
    balance_after_transaction = factory.Faker("random_int", min=100, max=10000)
    stripe_payment_intent_id = factory.Faker("uuid4")
    wallet_transaction_type = factory.Faker(
        "random_element", elements=["DEPOSIT", "SPEND"]
    )
    wallet_transaction_status = factory.Faker(
        "random_element", elements=["PENDING", "COMPLETED", "FAILED"]
    )
    created_at = factory.Faker("date_time_this_year")
    updated_at = factory.Faker("date_time_this_year")


@pytest_asyncio.fixture
async def organization_wallet_transaction_factory(async_session):
    OrganizationWalletTransactionFactory._meta.session = async_session
    return OrganizationWalletTransactionFactory
