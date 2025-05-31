async def test_exists_user(user_repository, user):
    exists = await user_repository.exists(email=user.email)
    assert exists is True

async def test_exists_user_not_found(user_repository, faker):
    exists = await user_repository.exists(email=faker.email())
    assert exists is False
