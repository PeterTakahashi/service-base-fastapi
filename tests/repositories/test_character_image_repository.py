import pytest
from app.v1.repositories.character_repository import CharacterRepository
from app.v1.repositories.character_image_repository import CharacterImageRepository
from app.db.session import get_async_session
from uuid import uuid4
from tests.factories.product_factory import create_product
from tests.factories.user_factory import create_user
from tests.factories.character_factory import create_character
from tests.factories.character_image_factory import create_character_image

pytestmark = pytest.mark.asyncio

async def test_list_character_images_by_character():
    async for session in get_async_session():
        user = await create_user(session)
        product = await create_product(session, user)
        character = await create_character(session, product)
        await create_character_image(session, character)

        repo = CharacterImageRepository(session)
        images = await repo.list_character_images_by_character(character_id=character.id, limit=10, offset=0)

        assert len(images) >= 1
        assert images[0].character_id == character.id
        break
async def test_list_character_images_by_character_with_sorting():
    async for session in get_async_session():
        user = await create_user(session)
        product = await create_product(session, user)
        character = await create_character(session, product)
        # Create multiple character images
        for _ in range(3):
            await create_character_image(session, character)
        repo = CharacterImageRepository(session)
        images = await repo.list_character_images_by_character(character_id=character.id, limit=10, offset=0, sort_by="created_at", sort_order="desc")
        assert len(images) >= 3
        assert images[0].character_id == character.id
        assert images[0].created_at >= images[1].created_at
        break
async def test_character_image_create():
    async for session in get_async_session():
        user = await create_user(session)
        product = await create_product(session, user)
        character = await create_character(session, product)

        repo = CharacterImageRepository(session)
        image = await repo.character_image_create(character_id=character.id)

        assert image.character_id == character.id
        assert image.created_at is not None
        break
async def test_character_image_exists():
    async for session in get_async_session():
        user = await create_user(session)
        product = await create_product(session, user)
        character = await create_character(session, product)
        image = await create_character_image(session, character)

        repo = CharacterImageRepository(session)
        exists = await repo.character_image_exists(character_id=image.character_id)

        assert exists is True
        break
async def test_get_character_image():
    async for session in get_async_session():
        user = await create_user(session)
        product = await create_product(session, user)
        character = await create_character(session, product)
        image = await create_character_image(session, character)

        repo = CharacterImageRepository(session)
        retrieved_image = await repo.get_character_image(character_image_id=image.id)

        assert retrieved_image.id == image.id
        assert retrieved_image.character_id == character.id
        break

async def test_delete_character_image():
    async for session in get_async_session():
        user = await create_user(session)
        product = await create_product(session, user)
        character = await create_character(session, product)
        image = await create_character_image(session, character)

        repo = CharacterImageRepository(session)
        deleted = await repo.delete_character_image(character_image_id=image.id)

        assert deleted is True
        retrieved_image = await repo.get_character_image(character_image_id=image.id)
        assert retrieved_image is None
        break
async def test_delete_character_image_not_found():
    async for session in get_async_session():
        user = await create_user(session)
        product = await create_product(session, user)
        character = await create_character(session, product)

        repo = CharacterImageRepository(session)
        deleted = await repo.delete_character_image(character_image_id=99999)

        assert deleted is False
        break