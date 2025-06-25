# pylint: disable=unused-import

import asyncio
import pytest
import pytest_asyncio
from app.core.startup import database
from app.db.session import get_async_session
from tests.fixtures.faker import *
from tests.fixtures.models import *
from tests.fixtures.repositories import *
from tests.fixtures.services import *
from tests.mocks.stripe import *
from tests.factories import *


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
