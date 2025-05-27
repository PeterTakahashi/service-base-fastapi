async def test_create_wallet_success(wallet_repository, user):
    stripe_customer_id = "cus_1234567890"

    wallet = await wallet_repository.create_wallet(user.id, stripe_customer_id)

    assert wallet.user_id == user.id
    assert wallet.stripe_customer_id == stripe_customer_id
    assert wallet.id is not None
