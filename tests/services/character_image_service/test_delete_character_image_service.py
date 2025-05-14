import pytest
from fastapi import HTTPException
from tests.common.check_error_response import check_not_found_status_code_and_detail
from app.lib.convert_id import encode_id
from app.core.response_type import forbidden_detail


@pytest.mark.asyncio
async def test_delete_character_image_success(
    character_image_service, user, character_image
):
    await character_image_service.delete_character_image(
        user_id=user.id,
        character_image_id=character_image.id,
    )
    # Check if the character image is soft deleted
    deleted_character_image = (
        await character_image_service.character_image_repository.get_character_image(
            character_image_id=character_image.id,
        )
    )
    assert deleted_character_image is None, "Character image should be soft deleted"


async def test_delete_character_image_not_found(character_image_service, user):
    character_image_id = 0
    with pytest.raises(HTTPException) as exc_info:
        await character_image_service.delete_character_image(
            user_id=user.id,
            character_image_id=character_image_id,
        )
    check_not_found_status_code_and_detail(
        exc_info.value.status_code,
        exc_info.value.detail,
        "CharacterImage",
        "character_image_id",
        encode_id(character_image_id),
    )


async def test_delete_character_image_forbidden(
    character_image_service, user, character_image
):
    # Simulate a different user trying to delete the character image
    different_user_id = "different_user_id"
    with pytest.raises(HTTPException) as exc_info:
        await character_image_service.delete_character_image(
            user_id=different_user_id,
            character_image_id=character_image.id,
        )
    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == forbidden_detail
