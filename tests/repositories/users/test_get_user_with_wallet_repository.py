async def test_get_user_with_wallet(user_repository, user, wallet):
    result = await user_repository.get_user_with_wallet(user.id)
    assert result is not None
    assert result.id == user.id
    assert result.email == user.email
    assert result.wallet is not None
    assert result.wallet.balance == wallet.balance
