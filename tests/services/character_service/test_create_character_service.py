from starlette.datastructures import UploadFile
import pytest
from fastapi import HTTPException


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
        character_image_files.append(
            UploadFile(filename=path.split("/")[-1], file=file)
        )

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


async def test_create_character_already_exists(
    character_service, product, character_with_character_images
):
    name = character_with_character_images.name

    with pytest.raises(HTTPException) as exc_info:
        await character_service.create_character(
            user_id=product.user_id,
            product_id=product.id,
            name=name,
            character_image_files=[],
        )

    assert exc_info.value.status_code == 409
    assert exc_info.value.detail == {
        "errors": [
            {
                "status": "409",
                "code": "character_already_exists",
                "title": "Conflict",
                "detail": f"Character with /name '{name}' already exists.",
                "source": {"pointer": "/name"},
            }
        ]
    }
