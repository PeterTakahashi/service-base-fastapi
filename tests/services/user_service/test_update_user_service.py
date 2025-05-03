from app.v1.schemas.user import UserUpdate, UserRead

async def test_update_me(user_service, user):
    update_data = UserUpdate(email="test@test.com", hashed_password="newpassword")
    result = await user_service.update_me(user, update_data)
    assert isinstance(result, UserRead)
    assert result.id == user.id
    assert result.email == update_data.email
