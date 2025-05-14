# pylint: disable=unused-import

import asyncio
import pytest
import pytest_asyncio
from app.core.startup import database
from app.db.session import get_async_session
from faker import Faker
from tests.fixtures.model_fixture import user
from tests.fixtures.repository_fixture import (
    user_repository,
)
from tests.fixtures.service_fixture import (
    user_service,
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
