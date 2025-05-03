import pytest_asyncio
from app.v1.repositories.character_image_repository import CharacterImageRepository

@pytest_asyncio.fixture
async def character_image_repository(async_session):
    return CharacterImageRepository(async_session)

async def test_list_character_images_by_character(character_image_repository, character_image):
    character_images = await character_image_repository.list_character_images_by_character(
        character_id=character_image.character.id, limit=10, offset=0
    )

    assert len(character_images) >= 1
    assert character_images[0].character_id == character_image.character.id

async def test_character_image_exists(character_image_repository, character_image):
    exists = await character_image_repository.character_image_exists(
        character_id=character_image.character.id
    )

    assert exists is True

async def test_character_image_not_exists(character_image_repository, character):
    exists = await character_image_repository.character_image_exists(
        character_id=character.id
    )

    assert exists is False

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
