import pytest
from app.v1.schemas.product import ProductCreate
from fastapi import HTTPException

async def test_create_product(product_service, user):
    data = ProductCreate(title="New Product")
    product = await product_service.create_product(user_id=str(user.id), data=data)

    assert product.title == "New Product"
    assert product.id is not None
    assert product.created_at is not None
    assert product.updated_at is not None

async def test_create_product_already_exists(product_service, product):
    data = ProductCreate(title=product.title)
    with pytest.raises(HTTPException) as exc_info:
        await product_service.create_product(user_id=str(product.user.id), data=data)

    assert exc_info.value.status_code == 409
    assert exc_info.value.detail == {
        "errors": [
            {
                "status": "409",
                "code": "product_already_exists",
                "title": "Conflict",
                "detail": f"Product with /title '{product.title}' already exists.",
                "source": {"pointer": "/title"},
            }
        ]
    }
