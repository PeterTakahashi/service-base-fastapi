import pytest_asyncio
from app.v1.services.payment_intent_service import PaymentIntentService


@pytest_asyncio.fixture
async def payment_intent_service(
    user_wallet_repository,
    user_wallet_transaction_repository,
    organization_wallet_repository,
    organization_wallet_transaction_repository,
):
    return PaymentIntentService(
        user_wallet_repository,
        user_wallet_transaction_repository,
        organization_wallet_repository,
        organization_wallet_transaction_repository,
    )
