from uuid import uuid4

async def test_list_products(product_repository, product):
    products = await product_repository.list_products(user_id=str(product.user.id), limit=10, offset=0)
    assert len(products) >= 1
    assert products[0][0].title == product.title

async def test_product_exists_true(product_repository, product):
    exists = await product_repository.product_exists(
        user_id=str(product.user.id), title=product.title
    )
    assert exists is True

async def test_product_exists_false(product_repository, user):
    exists = await product_repository.product_exists(
        user_id=str(user.id), title="NonExisting Product"
    )

    assert exists is False

async def test_create_product(product_repository, user):
    product = await product_repository.create_product(
        title="Created Product", user_id=str(user.id)
    )
    assert product.title == "Created Product"
    assert str(product.user_id) == str(user.id)

async def test_get_product_success(product_repository, product):
    fetched_product = await product_repository.get_product(
        user_id=str(product.user.id), product_display_id=str(product.display_id)
    )

    assert fetched_product is not None
    assert fetched_product.title == product.title

async def test_get_product_not_found(product_repository, user):
    fetched_product = await product_repository.get_product(user_id=str(user.id), product_display_id=str(uuid4()))

    assert fetched_product is None

async def test_update_product(product_repository, product):
    updated_product = await product_repository.update_product(
        product=product, data={"title": "After Update"}
    )

    assert updated_product.title == "After Update"

async def test_soft_delete_product(product_repository, product):
    await product_repository.soft_delete_product(product)

    # 削除後に通常取得するとNoneになるはず
    fetched_product = await product_repository.get_product(
            user_id=str(product.user.id), product_display_id=str(product.display_id)
        )
    assert fetched_product is None
