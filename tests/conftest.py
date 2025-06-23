# pylint: disable=unused-import

import asyncio
import pytest
import pytest_asyncio
from app.core.startup import database
from app.db.session import get_async_session
from faker import Faker
from tests.fixtures.models import (
    user,
    other_user,
    users,
    user_wallet,
    other_user_wallet,
    user_wallets,
    user_wallet_transaction,
    other_user_wallet_transaction,
    user_api_key,
    soft_deleted_user_api_key,
    user_api_keys,
    expired_user_api_key,
    user_api_key_with_expires_at,
    organization,
    soft_deleted_organization,
    organizations,
)
from tests.fixtures.repositories import (
    user_repository,
    user_wallet_repository,
    user_wallet_transaction_repository,
    user_api_key_repository,
    organization_repository,
)
from tests.fixtures.services import (
    user_service,
    payment_intent_service,
    user_wallet_transaction_service,
    user_api_key_service,
    organization_service,
)
from tests.mocks.stripe import (
    mock_stripe_customer_create,
    mock_payment_intent_create_patch,
)
from tests.factories import (
    user_factory,
    user_wallet_factory,
    user_wallet_transaction_factory,
    user_api_key_factory,
    organization_factory,
)


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_database():
    await database.connect()
    yield
    await database.disconnect()


@pytest_asyncio.fixture(autouse=True)
async def clean_tables():
    for table in [
        "users",
    ]:
        await database.execute(f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE")


@pytest_asyncio.fixture
async def async_session():
    async for session in get_async_session():
        yield session


@pytest_asyncio.fixture
def faker():
    return Faker()
