import pytest_asyncio
from app.v1.repositories.character_repository import CharacterRepository

@pytest_asyncio.fixture
async def character_repository(async_session):
    return CharacterRepository(async_session)

async def test_list_characters_by_product(character_repository, character):
    characters = await character_repository.list_characters_by_product(product_id=character.product.id, limit=10, offset=0)

    assert len(characters) >= 1
    assert characters[0].name == character.name
    assert characters[0].product_id ==character.product.id

async def test_list_characters_by_product_with_name_filter(character_repository, character):
    product = character.product
    characters = await character_repository.list_characters_by_product(product_id=product.id, limit=10, offset=0, name=character.name)

    assert len(characters) >= 1
    assert characters[0].name == character.name
    assert characters[0].product_id == product.id

async def test_character_exists(character_repository, character):
    exists = await character_repository.character_exists(product_id=character.product.id, name=character.name)

    assert exists is True

async def test_character_not_exists(character_repository, character):
    exists = await character_repository.character_exists(product_id=character.product.id, name="NonExisting Character")

    assert exists is False

async def test_create_character(character_repository, product):
    character = await character_repository.create_character(name="New Character", product_id=product.id)
    assert character.name == "New Character"
    assert character.product_id == product.id
    assert character.id is not None

async def test_get_character(character_repository, character):
    fetched_character = await character_repository.get_character(character_id=character.id)

    assert fetched_character is not None
    assert fetched_character.name == character.name
    assert fetched_character.product_id == character.product.id

async def test_get_character_not_found(character_repository):
    fetched_character = await character_repository.get_character(character_id=99999999)

    assert fetched_character is None

async def test_update_character(character_repository, character):
    updated_character = await character_repository.update_character(character=character, data={"name": "Updated Character"})

    assert updated_character.name == "Updated Character"
    assert updated_character.product_id == character.product.id

async def test_soft_delete_character(character_repository, character):
    await character_repository.soft_delete_character(character)

    fetched_character = await character_repository.get_character(character_id=character.id)
    assert fetched_character is None
