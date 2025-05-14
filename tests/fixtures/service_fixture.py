import pytest_asyncio
from app.v1.services.product_service import ProductService
from app.v1.services.character_service import CharacterService
from app.v1.services.user_service import UserService
from app.v1.services.character_image_service import CharacterImageService


@pytest_asyncio.fixture
async def character_service(
    product_repository, character_repository, character_image_repository
):
    return CharacterService(
        product_repository, character_repository, character_image_repository
    )


@pytest_asyncio.fixture
async def product_service(product_repository):
    return ProductService(product_repository)


@pytest_asyncio.fixture
async def user_service(user_repository):
    return UserService(user_repository)


@pytest_asyncio.fixture
async def character_image_service(
    product_repository, character_repository, character_image_repository
):
    return CharacterImageService(
        product_repository, character_repository, character_image_repository
    )
