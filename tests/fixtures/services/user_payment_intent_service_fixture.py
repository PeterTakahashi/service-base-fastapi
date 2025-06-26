import pytest_asyncio
from app.v1.services.user_payment_intent_service import UserPaymentIntentService


@pytest_asyncio.fixture
async def user_payment_intent_service(
    user_wallet_repository, user_wallet_transaction_repository
):
    return UserPaymentIntentService(
        user_wallet_repository, user_wallet_transaction_repository
    )
