from starlette.datastructures import UploadFile
import pytest_asyncio

@pytest_asyncio.fixture
async def character_service(product_repository, character_repository, character_image_repository):
    from app.v1.services.character_service import CharacterService
    return CharacterService(product_repository, character_repository, character_image_repository)

async def test_create_character_with_real_images(character_service, product, faker):
    name = faker.name()

    # ファイルを開いて UploadFile に変換
    file_paths = [
        "tests/files/character_image/1.png",
        "tests/files/character_image/2.png",
    ]
    image_files = []
    for path in file_paths:
        file = open(path, "rb")  # rbモードで開く
        image_files.append(UploadFile(filename=path.split("/")[-1], file=file))

    character = await character_service.create_character(
        user_id=product.user_id,
        product_id=product.id,
        name=name,
        image_files=image_files,
    )

    # クローズ忘れずに
    for f in image_files:
        await f.close()

    assert character.name == name
    assert character.product_id == product.id
    assert character.id is not None
    assert len(character.character_images) == len(image_files)
    assert character.character_images[0].id is not None
    assert character.character_images[0].image_url is not None
    assert character.character_images[1].id is not None
    assert character.character_images[1].image_url is not None