from starlette.datastructures import UploadFile
import pytest_asyncio

@pytest_asyncio.fixture
async def character_service(product_repository, character_repository, character_image_repository):
    from app.v1.services.character_service import CharacterService
    return CharacterService(product_repository, character_repository, character_image_repository)

async def test_get_character(character_service, product, character_with_character_images):
    character = character_with_character_images
    character_read = await character_service.get_character(
        user_id=product.user_id,
        product_id=product.id,
        character_id=character.id,
    )

    assert character_read.id == character.id
    assert character_read.name == character.name
    assert character_read.product_id == product.id
    assert character_read.character_images[0].id == character.character_images[0].id
    assert character_read.character_images[0].image_url is not None
    assert character_read.character_images[1].id == character.character_images[1].id
    assert character_read.character_images[1].image_url is not None

async def test_create_character_with_real_images(character_service, product, faker):
    name = faker.name()

    # ファイルを開いて UploadFile に変換
    file_paths = [
        "tests/files/character_image/1.png",
        "tests/files/character_image/2.png",
    ]
    character_image_files = []
    for path in file_paths:
        file = open(path, "rb")  # rbモードで開く
        character_image_files.append(UploadFile(filename=path.split("/")[-1], file=file))

    character = await character_service.create_character(
        user_id=product.user_id,
        product_id=product.id,
        name=name,
        character_image_files=character_image_files,
    )

    # クローズ忘れずに
    for f in character_image_files:
        await f.close()

    assert character.name == name
    assert character.product_id == product.id
    assert character.id is not None
    assert len(character.character_images) == len(character_image_files)
    assert character.character_images[0].id is not None
    assert character.character_images[0].image_url is not None
    assert character.character_images[1].id is not None
    assert character.character_images[1].image_url is not None