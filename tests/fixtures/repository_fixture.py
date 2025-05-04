import pytest_asyncio
from app.v1.repositories.product_repository import ProductRepository
from app.v1.repositories.user_repository import UserRepository
from app.v1.repositories.character_repository import CharacterRepository
from app.v1.repositories.character_image_repository import CharacterImageRepository


@pytest_asyncio.fixture
async def product_repository(async_session):
    return ProductRepository(async_session)


@pytest_asyncio.fixture
async def user_repository(async_session):
    return UserRepository(async_session)


@pytest_asyncio.fixture
async def character_repository(async_session):
    return CharacterRepository(async_session)


@pytest_asyncio.fixture
async def character_image_repository(async_session):
    return CharacterImageRepository(async_session)
