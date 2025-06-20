import pytest_asyncio


@pytest_asyncio.fixture
async def user_wallet_transaction(
    async_session, user_wallet, user_wallet_transaction_factory
):
    transaction = await user_wallet_transaction_factory.create(user_wallet=user_wallet)
    return transaction


@pytest_asyncio.fixture
async def other_user_wallet_transaction(
    async_session, other_user_wallet, user_wallet_transaction_factory
):
    transaction = await user_wallet_transaction_factory.create(
        user_wallet=other_user_wallet
    )
    return transaction
