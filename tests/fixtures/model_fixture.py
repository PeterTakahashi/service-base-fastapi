import pytest_asyncio
from tests.factories.user_factory import UserFactory
from tests.factories.product_factory import ProductFactory
from tests.factories.character_factory import CharacterFactory
from tests.factories.character_image_factory import CharacterImageFactory
from datetime import datetime

@pytest_asyncio.fixture
async def user(async_session):
    UserFactory._meta.session = async_session
    user = await UserFactory.create()
    return user


@pytest_asyncio.fixture
async def product(async_session, user):
    ProductFactory._meta.session = async_session
    product = await ProductFactory.create(user=user)
    return product


@pytest_asyncio.fixture
async def product_with_characters(async_session, user):
    ProductFactory._meta.session = async_session
    CharacterFactory._meta.session = async_session
    product = await ProductFactory.create(user=user)
    await CharacterFactory.create(product=product)
    await CharacterFactory.create(product=product)
    await async_session.refresh(product, ["characters"])
    return product


@pytest_asyncio.fixture
async def character(async_session, product):
    CharacterFactory._meta.session = async_session
    character = await CharacterFactory.create(product=product)
    return character


@pytest_asyncio.fixture
async def character_with_character_images(async_session, product):
    CharacterFactory._meta.session = async_session
    CharacterImageFactory._meta.session = async_session
    character = await CharacterFactory.create(product=product)
    await CharacterImageFactory.create(character=character)
    await CharacterImageFactory.create(character=character)
    # Explicitly load the relationship to avoid lazy loading
    await async_session.refresh(character, ["character_images"])
    return character

@pytest_asyncio.fixture
async def character_with_soft_deleted_character_images(async_session, product):
    CharacterFactory._meta.session = async_session
    CharacterImageFactory._meta.session = async_session
    character = await CharacterFactory.create(product=product)
    await CharacterImageFactory.create(character=character, deleted_at=datetime.utcnow())
    await CharacterImageFactory.create(character=character, deleted_at=datetime.utcnow())
    # Explicitly load the relationship to avoid lazy loading
    await async_session.refresh(character, ["character_images"])
    return character


@pytest_asyncio.fixture
async def character_image(async_session, character):
    CharacterImageFactory._meta.session = async_session
    character_image = await CharacterImageFactory.create(character=character)
    return character_image
