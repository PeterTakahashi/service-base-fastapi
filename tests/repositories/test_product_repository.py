import pytest
from app.repositories.product_repository import ProductRepository
from app.db.session import get_async_session
from tests.factories.product_factory import create_product
from tests.factories.user_factory import create_user
from uuid import uuid4

pytestmark = pytest.mark.asyncio


async def test_list_products():
    async for session in get_async_session():
        user = await create_user(session)
        await create_product(session, user, title="Repository Test Product")

        repo = ProductRepository(session)
        products = await repo.list_products(user_id=str(user.id), limit=10, offset=0)

        assert len(products) >= 1
        assert products[0][0].title == "Repository Test Product"
        break


async def test_product_exists_true():
    async for session in get_async_session():
        user = await create_user(session)
        await create_product(session, user, title="Existing Product")

        repo = ProductRepository(session)
        exists = await repo.product_exists(
            user_id=str(user.id), title="Existing Product"
        )

        assert exists is True
        break


async def test_product_exists_false():
    async for session in get_async_session():
        user = await create_user(session)

        repo = ProductRepository(session)
        exists = await repo.product_exists(
            user_id=str(user.id), title="NonExisting Product"
        )

        assert exists is False
        break


async def test_create_product():
    async for session in get_async_session():
        user = await create_user(session)

        repo = ProductRepository(session)
        product = await repo.create_product(
            title="Created Product", user_id=str(user.id)
        )

        assert product.title == "Created Product"
        assert str(product.user_id) == str(user.id)
        break


async def test_get_product_success():
    async for session in get_async_session():
        user = await create_user(session)
        created_product = await create_product(session, user, title="Get Test Product")

        repo = ProductRepository(session)
        product = await repo.get_product(
            user_id=str(user.id), display_id=str(created_product.display_id)
        )

        assert product is not None
        assert product.title == "Get Test Product"
        break


async def test_get_product_not_found():
    async for session in get_async_session():
        user = await create_user(session)

        repo = ProductRepository(session)
        product = await repo.get_product(user_id=str(user.id), display_id=str(uuid4()))

        assert product is None
        break


async def test_update_product():
    async for session in get_async_session():
        user = await create_user(session)
        created_product = await create_product(session, user, title="Before Update")

        repo = ProductRepository(session)
        updated_product = await repo.update_product(
            product=created_product, data={"title": "After Update"}
        )

        assert updated_product.title == "After Update"
        break


async def test_soft_delete_product():
    async for session in get_async_session():
        user = await create_user(session)
        created_product = await create_product(
            session, user, title="Soft Delete Product"
        )

        repo = ProductRepository(session)
        await repo.soft_delete_product(created_product)

        # 削除後に通常取得するとNoneになるはず
        product = await repo.get_product(
            user_id=str(user.id), display_id=str(created_product.display_id)
        )
        assert product is None
        break
