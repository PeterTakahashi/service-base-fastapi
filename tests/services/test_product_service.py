import pytest
from unittest.mock import AsyncMock
from app.services.product_service import ProductService
from app.schemas.product import ProductCreate, ProductUpdate
from app.models.product import Product
from uuid import uuid4
from datetime import datetime
from fastapi import HTTPException

pytestmark = pytest.mark.asyncio

@pytest.fixture
def mock_repository():
    return AsyncMock()

@pytest.fixture
def product_service(mock_repository):
    return ProductService(product_repository=mock_repository)

@pytest.fixture
def sample_product():
    return Product(
        id=1,
        display_id=uuid4(),
        title="Sample Product",
        user_id=uuid4(),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        deleted_at=None,
    )

async def test_list_products(product_service, mock_repository, sample_product):
    mock_repository.list_products.return_value = [(sample_product, 3)]

    user_id = str(uuid4())
    result = await product_service.list_products(user_id)

    assert len(result) == 1
    assert result[0].title == sample_product.title

async def test_create_product_success(product_service, mock_repository, sample_product):
    user_id = str(uuid4())
    data = ProductCreate(title="New Product")

    mock_repository.product_exists.return_value = False
    mock_repository.create_product.return_value = sample_product

    result = await product_service.create_product(user_id, data)

    assert result.title == sample_product.title
    mock_repository.create_product.assert_called_once()

async def test_create_product_conflict(product_service, mock_repository):
    user_id = str(uuid4())
    data = ProductCreate(title="Duplicate")

    mock_repository.product_exists.return_value = True

    with pytest.raises(HTTPException) as exc_info:
        await product_service.create_product(user_id, data)

    assert exc_info.value.status_code == 409

async def test_get_product_success(product_service, mock_repository, sample_product):
    user_id = str(uuid4())
    product_id = str(uuid4())

    mock_repository.get_product.return_value = sample_product

    result = await product_service.get_product(user_id, product_id)

    assert result.title == sample_product.title

async def test_get_product_not_found(product_service, mock_repository):
    user_id = str(uuid4())
    product_id = str(uuid4())

    mock_repository.get_product.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        await product_service.get_product(user_id, product_id)

    assert exc_info.value.status_code == 404

async def test_update_product_success(product_service, mock_repository, sample_product):
    user_id = str(uuid4())
    product_id = str(uuid4())
    data = ProductUpdate(title="Updated Title")

    mock_repository.get_product.return_value = sample_product
    mock_repository.update_product.return_value = sample_product

    result = await product_service.update_product(user_id, product_id, data)

    assert result.title == sample_product.title

async def test_update_product_not_found(product_service, mock_repository):
    user_id = str(uuid4())
    product_id = str(uuid4())
    data = ProductUpdate(title="Title")

    mock_repository.get_product.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        await product_service.update_product(user_id, product_id, data)

    assert exc_info.value.status_code == 404

async def test_delete_product_success(product_service, mock_repository, sample_product):
    user_id = str(uuid4())
    product_id = str(uuid4())

    mock_repository.get_product.return_value = sample_product

    await product_service.delete_product(user_id, product_id)

    mock_repository.soft_delete_product.assert_called_once_with(sample_product)

async def test_delete_product_not_found(product_service, mock_repository):
    user_id = str(uuid4())
    product_id = str(uuid4())

    mock_repository.get_product.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        await product_service.delete_product(user_id, product_id)

    assert exc_info.value.status_code == 404
