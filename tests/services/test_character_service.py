import pytest_asyncio
from app.v1.services.character_service import CharacterService

@pytest_asyncio.fixture
async def character_service(product_repository, character_repository):
    return CharacterService(product_repository, character_repository)
