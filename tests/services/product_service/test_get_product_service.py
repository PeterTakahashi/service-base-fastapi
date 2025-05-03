import pytest
from fastapi import HTTPException
from app.lib.convert_id import encode_id

async def test_get_product_success(product_service, product):
    fetched_product = await product_service.get_product(
        user_id=str(product.user.id), product_id=product.id
    )

    assert fetched_product is not None
    assert fetched_product.title == product.title
    assert fetched_product.id == product.id
    assert fetched_product.created_at is not None
    assert fetched_product.updated_at is not None

async def test_get_product_not_found(product_service, user):
    product_id = 0
    with pytest.raises(HTTPException) as exc_info:
        await product_service.get_product(
            user_id=str(user.id), product_id=product_id
        )

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == {
        "errors": [
            {
                "status": "404",
                "code": "product_not_found",
                "title": "Not Found",
                "detail": f"Product with id '{encode_id(product_id)}' not found.",
                "source": {"pointer": "/product_id"},
            }
        ]
    }
