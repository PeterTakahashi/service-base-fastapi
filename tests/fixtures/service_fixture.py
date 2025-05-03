import pytest_asyncio

@pytest_asyncio.fixture
async def character_service(product_repository, character_repository, character_image_repository):
    from app.v1.services.character_service import CharacterService
    return CharacterService(product_repository, character_repository, character_image_repository)
