from app.v1.schemas.user import UserRead


async def test_get_me(user_service, user, user_wallet):
    result = await user_service.get_me(user)
    assert isinstance(result, UserRead)
    assert result.id == user.id
    assert result.email == user.email
    assert result.user_wallet is not None
    assert result.user_wallet.balance == user_wallet.balance
    assert result.address is not None
    assert result.address.country is not None
