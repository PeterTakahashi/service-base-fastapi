import asyncio
import pytest
import pytest_asyncio
from app.core.startup import database
from app.db.session import get_async_session
from faker import Faker
from tests.fixtures.model_fixture import (
    user,
    product,
    product_with_characters,
    character,
    character_with_character_images,
    character_image,
)
from tests.fixtures.repository_fixture import (
    character_repository,
    product_repository,
    character_image_repository,
    user_repository,
)
from tests.fixtures.service_fixture import (
    character_service,
    product_service,
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
        "pages",
        "episodes",
        "character_images",
        "characters",
        "products",
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
