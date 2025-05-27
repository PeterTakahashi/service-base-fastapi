import pytest_asyncio
from tests.factories.user_factory import UserFactory
from tests.factories.wallet_factory import WalletFactory
from tests.factories.wallet_transaction_factory import WalletTransactionFactory


@pytest_asyncio.fixture
async def user(async_session):
    UserFactory._meta.session = async_session
    user = await UserFactory.create()
    return user


@pytest_asyncio.fixture
async def wallet(async_session, user):
    WalletFactory._meta.session = async_session
    wallet = await WalletFactory.create(user=user)
    return wallet


@pytest_asyncio.fixture
async def wallet_transaction(async_session, wallet):
    WalletTransactionFactory._meta.session = async_session
    transaction = await WalletTransactionFactory.create(wallet=wallet)
    return transaction
