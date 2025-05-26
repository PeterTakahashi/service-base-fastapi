
async def test_get_wallet_success(wallet_repository, user, wallet):
    retrieved_wallet = await wallet_repository.get_wallet_by_user_id(user.id)

    assert retrieved_wallet is not None
    assert retrieved_wallet.id == wallet.id
    assert retrieved_wallet.user_id == user.id
    assert retrieved_wallet.stripe_customer_id == wallet.stripe_customer_id