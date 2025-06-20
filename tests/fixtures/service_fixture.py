import pytest_asyncio
from app.v1.services.user_service import UserService
from app.v1.services.payment_intent_service import PaymentIntentService
from app.v1.services.user_wallet_transaction_service import UserWalletTransactionService
from app.v1.services.user_api_key_service import UserApiKeyService


@pytest_asyncio.fixture
async def user_service(user_repository):
    return UserService(user_repository)


@pytest_asyncio.fixture
async def payment_intent_service(
    user_wallet_repository, user_wallet_transaction_repository
):
    return PaymentIntentService(
        user_wallet_repository, user_wallet_transaction_repository
    )


@pytest_asyncio.fixture
async def user_wallet_transaction_service(user_wallet_transaction_repository):
    return UserWalletTransactionService(user_wallet_transaction_repository)


@pytest_asyncio.fixture
async def user_api_key_service(user_api_key_repository):
    return UserApiKeyService(user_api_key_repository)
