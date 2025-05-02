import pytest
import pytest_asyncio
from app.v1.services.product_service import ProductService
from app.v1.schemas.product import ProductCreate, ProductUpdate
from fastapi import HTTPException
from app.lib.convert_id import encode_id

@pytest_asyncio.fixture
async def product_service(product_repository):
    return ProductService(product_repository)

async def test_list_products(product_service, product):
    products = await product_service.list_products(user_id=str(product.user.id), limit=10, offset=0)
    assert len(products) >= 1
    assert products[0].title == product.title

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
                "detail": f"Product with title '{product.title}' already exists.",
                "source": {"pointer": "/title"},
            }
        ]
    }

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
                "detail": f"Product with title '{existing_product.title}' already exists.",
                "source": {"pointer": "/title"},
            }
        ]
    }

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