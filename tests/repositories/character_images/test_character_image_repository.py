import pytest_asyncio
from app.v1.repositories.character_image_repository import CharacterImageRepository

@pytest_asyncio.fixture
async def character_image_repository(async_session):
    return CharacterImageRepository(async_session)

async def test_create_character_image(character_image_repository, character):
    character_image = await character_image_repository.character_image_create(
        character_id=character.id
    )
    assert character_image.character_id == character.id
    assert character_image.created_at is not None
    assert character_image.updated_at is not None

async def test_get_character_image(character_image_repository, character_image):
    fetched_character_image = await character_image_repository.get_character_image(
        character_image_id=character_image.id
    )

    assert fetched_character_image is not None
    assert fetched_character_image.character_id == character_image.character.id
    assert fetched_character_image.id == character_image.id

async def test_get_character_image_not_found(character_image_repository):
    fetched_character_image = await character_image_repository.get_character_image(
        character_image_id=99999999
    )

    assert fetched_character_image is None

async def test_update_character_image_storage_key(
    character_image_repository, character_image
):
    updated_character_image = await character_image_repository.update_character_image_storage_key(
        character_image=character_image, storage_key="new_storage_key"
    )

    assert updated_character_image.storage_key == "new_storage_key"
    assert updated_character_image.updated_at is not None

async def test_soft_delete_character_image(character_image_repository, character_image):
    await character_image_repository.soft_delete_character_image(character_image)

    fetched_character_image = await character_image_repository.get_character_image(
        character_image_id=character_image.id
    )

    assert fetched_character_image is None
