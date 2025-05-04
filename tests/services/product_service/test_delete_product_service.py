import pytest
from fastapi import HTTPException
from app.lib.convert_id import encode_id


async def test_delete_product(product_service, product):
    await product_service.delete_product(
        user_id=str(product.user.id), product_id=product.id
    )

    # 削除後に通常取得するとNoneになるはず
    with pytest.raises(HTTPException) as exc_info:
        await product_service.get_product(
            user_id=str(product.user.id), product_id=product.id
        )

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == {
        "errors": [
            {
                "status": "404",
                "code": "product_not_found",
                "title": "Not Found",
                "detail": f"Product with id '{encode_id(product.id)}' not found.",
                "source": {"pointer": "/product_id"},
            }
        ]
    }


async def test_delete_product_not_found(product_service, user):
    product_id = 0
    with pytest.raises(HTTPException) as exc_info:
        await product_service.delete_product(
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
