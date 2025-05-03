
async def test_list_products(product_service, product):
    products = await product_service.list_products(user_id=str(product.user.id), limit=10, offset=0)
    assert len(products) >= 1
    assert products[0].title == product.title
