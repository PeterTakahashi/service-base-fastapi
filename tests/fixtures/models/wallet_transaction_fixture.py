import pytest_asyncio


@pytest_asyncio.fixture
async def wallet_transaction(async_session, wallet, wallet_transaction_factory):
    transaction = await wallet_transaction_factory.create(wallet=wallet)
    return transaction


@pytest_asyncio.fixture
async def other_wallet_transaction(
    async_session, other_wallet, wallet_transaction_factory
):
    transaction = await wallet_transaction_factory.create(wallet=other_wallet)
    return transaction
