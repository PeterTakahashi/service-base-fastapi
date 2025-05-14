from starlette.datastructures import UploadFile
import pytest
from fastapi import HTTPException
from app.core.config import settings
from tests.common.check_error_response import check_not_found_status_code_and_detail
from app.lib.convert_id import encode_id


async def test_add_character_images_with_real_images(
    character_service, product, character_with_character_images, faker
):
    # 1. create a character
    name = faker.name()
    character = await character_service.create_character(
        user_id=product.user_id,
        product_id=product.id,
        name=name,
        character_image_files=[],
    )

    # 2. add images to the character
    file_paths = [
        "tests/files/character_image/1.png",
        "tests/files/character_image/2.png",
    ]
    character_image_files = []
    for path in file_paths:
        file = open(path, "rb")
        character_image_files.append(
            UploadFile(filename=path.split("/")[-1], file=file)
        )

    updated_character = await character_service.add_character_images(
        user_id=product.user_id,
        product_id=product.id,
        character_id=character.id,
        character_image_files=character_image_files,
    )

    for f in character_image_files:
        await f.close()

    assert updated_character.id == character.id
    assert updated_character.name == name
    assert updated_character.product_id == product.id
    assert len(updated_character.character_images) == len(character_image_files)
    assert updated_character.character_images[0].id is not None
    assert updated_character.character_images[0].image_url is not None
    assert updated_character.character_images[1].id is not None
    assert updated_character.character_images[1].image_url is not None


async def test_add_character_images_not_found_product(
    character_service, user, character_with_character_images
):
    with pytest.raises(HTTPException) as exc_info:
        await character_service.add_character_images(
            user_id=user.id,
            product_id=0,
            character_id=character_with_character_images.id,
            character_image_files=[],
        )

    check_not_found_status_code_and_detail(
        exc_info.value.status_code,
        exc_info.value.detail,
        "Product",
        "product_id",
        encode_id(0),
    )


async def test_add_character_images_not_found_character(
    character_service, product, character_with_character_images
):
    with pytest.raises(HTTPException) as exc_info:
        await character_service.add_character_images(
            user_id=product.user_id,
            product_id=product.id,
            character_id=0,
            character_image_files=[],
        )

    check_not_found_status_code_and_detail(
        exc_info.value.status_code,
        exc_info.value.detail,
        "Character",
        "character_id",
        encode_id(0),
    )


async def test_add_character_images_over_max_images(
    character_service, product, character_with_character_images
):
    # ファイルを開いて UploadFile に変換
    file_paths = []
    for i in range(11):
        file_paths.append(f"tests/files/character_image/{i + 1}.png")
    character_image_files = []
    for path in file_paths:
        file = open(path, "rb")  # rbモードで開く
        character_image_files.append(
            UploadFile(filename=path.split("/")[-1], file=file)
        )

    with pytest.raises(HTTPException) as exc_info:
        await character_service.add_character_images(
            user_id=product.user_id,
            product_id=product.id,
            character_id=character_with_character_images.id,
            character_image_files=character_image_files,
        )
    for f in character_image_files:
        await f.close()

    assert exc_info.value.status_code == 422
    assert exc_info.value.detail == {
        "errors": [
            {
                "status": "422",
                "code": "invalid_request",
                "title": "Unprocessable Entity",
                "detail": f"Character image count must be between 1 and {settings.MAX_CHARACTER_IMAGES_COUNT}.",
                "source": {"parameter": "character_image_files"},
            }
        ]
    }
