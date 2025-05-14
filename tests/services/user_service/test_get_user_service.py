from app.v1.schemas.user import UserRead


async def test_get_me(user_service, user):
    result = await user_service.get_me(user)
    assert isinstance(result, UserRead)
    assert result.id == user.id
    assert result.email == user.email
