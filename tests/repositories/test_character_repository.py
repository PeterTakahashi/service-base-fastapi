import pytest
from app.v1.repositories.character_repository import CharacterRepository
from app.db.session import get_async_session
from tests.factories.product_factory import create_product
from tests.factories.user_factory import create_user
from tests.factories.character_factory import create_character
from uuid import uuid4

pytestmark = pytest.mark.asyncio

async def test_list_characters_by_product():
    async for session in get_async_session():
        user = await create_user(session)
        product = await create_product(session, user)
        await create_character(session, product, name="Repository Test Character")

        repo = CharacterRepository(session)
        characters = await repo.list_characters_by_product(product_id=product.id, limit=10, offset=0)

        assert len(characters) >= 1
        assert characters[0].name == "Repository Test Character"
        assert characters[0].product_id == product.id
        break

async def test_list_characters_by_product_with_name_filter():
    async for session in get_async_session():
        user = await create_user(session)
        product = await create_product(session, user)
        await create_character(session, product, name="Repository Test Character")

        repo = CharacterRepository(session)
        characters = await repo.list_characters_by_product(product_id=product.id, limit=10, offset=0, name="Test")

        assert len(characters) >= 1
        assert characters[0].name == "Repository Test Character"
        assert characters[0].product_id == product.id
        break

async def test_list_characters_by_product_with_sorting():
    async for session in get_async_session():
        user = await create_user(session)
        product = await create_product(session, user)
        # Create multiple characters
        await create_character(session, product, name="A Character")
        await create_character(session, product, name="B Character")
        await create_character(session, product, name="C Character")

        repo = CharacterRepository(session)
        characters = await repo.list_characters_by_product(product_id=product.id, limit=10, offset=0, sort_by="name", sort_order="desc")
        assert len(characters) == 3
        assert characters[0].name == "C Character"
        assert characters[1].name == "B Character"
        assert characters[2].name == "A Character"
        break

async def test_character_exists():
    async for session in get_async_session():
        user = await create_user(session)
        product = await create_product(session, user)
        character = await create_character(session, product, name="Repository Test Character")

        repo = CharacterRepository(session)
        exists = await repo.character_exists(product_id=product.id, name=character.name)

        assert exists is True
        break

async def test_character_not_exists():
    async for session in get_async_session():
        user = await create_user(session)
        product = await create_product(session, user)

        repo = CharacterRepository(session)
        exists = await repo.character_exists(product_id=product.id, name="Nonexistent Character")

        assert exists is False
        break

async def test_create_character():
    async for session in get_async_session():
        user = await create_user(session)
        product = await create_product(session, user)

        repo = CharacterRepository(session)
        character = await repo.create_character(name="New Character", product_id=product.id, display_id=str(uuid4()))

        assert character.name == "New Character"
        assert character.product_id == product.id
        assert character.display_id is not None
        break

async def test_get_character():
    async for session in get_async_session():
        user = await create_user(session)
        product = await create_product(session, user)
        character = await create_character(session, product, name="Repository Test Character")

        repo = CharacterRepository(session)
        fetched_character = await repo.get_character(character_id=character.id)

        assert fetched_character is not None
        assert fetched_character.name == "Repository Test Character"
        assert fetched_character.product_id == product.id
        break

async def test_get_character_not_found():
    async for session in get_async_session():
        user = await create_user(session)
        product = await create_product(session, user)

        repo = CharacterRepository(session)
        fetched_character = await repo.get_character(character_id=99999)  # Nonexistent ID

        assert fetched_character is None
        break

async def test_update_character():
    async for session in get_async_session():
        user = await create_user(session)
        product = await create_product(session, user)
        character = await create_character(session, product, name="Repository Test Character")

        repo = CharacterRepository(session)
        updated_character = await repo.update_character(character, {"name": "Updated Character"})

        assert updated_character.name == "Updated Character"
        assert updated_character.product_id == product.id
        break

async def test_soft_delete_character():
    async for session in get_async_session():
        user = await create_user(session)
        product = await create_product(session, user)
        character = await create_character(session, product, name="Repository Test Character")

        repo = CharacterRepository(session)
        await repo.soft_delete_character(character)

        deleted_character = await repo.get_character(character_id=character.id)

        assert deleted_character is None
        break