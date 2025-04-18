import asyncio
import pytest
import pytest_asyncio
from app.db.database import database

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
    # テーブルの順番に注意（外部キー制約）
    for table in ["pages", "users"]:
        await database.execute(f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE")
