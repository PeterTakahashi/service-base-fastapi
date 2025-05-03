import pytest
from app.v1.schemas.product import ProductCreate, ProductUpdate
from fastapi import HTTPException
from app.lib.convert_id import encode_id

async def test_update_product(product_service, product):
    data = ProductUpdate(title="Updated Product")
    updated_product = await product_service.update_product(
        user_id=str(product.user.id), product_id=product.id, data=data
    )

    assert updated_product.title == "Updated Product"
    assert updated_product.id == product.id
    assert updated_product.created_at == product.created_at
    assert updated_product.updated_at is not None

async def test_update_product_not_found(product_service, user):
    data = ProductUpdate(title="Updated Product")
    product_id = 0
    with pytest.raises(HTTPException) as exc_info:
        await product_service.update_product(
            user_id=str(user.id), product_id=product_id, data=data
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

async def test_update_product_already_exists(product_service, product):
    existing_product = await product_service.create_product(
        user_id=str(product.user.id), data=ProductCreate(title="Existing Product")
    )
    data = ProductUpdate(title=existing_product.title)
    with pytest.raises(HTTPException) as exc_info:
        await product_service.update_product(
            user_id=str(product.user.id), product_id=product.id, data=data
        )

    assert exc_info.value.status_code == 409
    assert exc_info.value.detail == {
        "errors": [
            {
                "status": "409",
                "code": "product_already_exists",
                "title": "Conflict",
                "detail": f"Product with /title '{existing_product.title}' already exists.",
                "source": {"pointer": "/title"},
            }
        ]
    }
