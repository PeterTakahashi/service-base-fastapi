import pytest
from fastapi import HTTPException

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

async def test_get_character_not_found_by_product_id(character_service, user):
    with pytest.raises(HTTPException) as exc_info:
        await character_service.get_character(
            user_id=user.id,
            product_id=0,
            character_id=0,
        )

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == {
        'errors': [
            {
                'status': '404',
                'code': 'product_not_found',
                'title': 'Not Found',
                'detail': "Product with id '0' not found.",
                'source': {
                    'pointer': '/product_id'
                }
            }
        ]
    }

async def test_get_character_not_found_by_character_id(character_service, product):
    with pytest.raises(HTTPException) as exc_info:
        await character_service.get_character(
            user_id=product.user_id,
            product_id=product.id,
            character_id=0,
        )

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == {
        'errors': [
            {
                'status': '404',
                'code': 'character_not_found',
                'title': 'Not Found',
                'detail': "Character with id '0' not found.",
                'source': {
                    'pointer': '/character_id'
                }
            }
        ]
    }