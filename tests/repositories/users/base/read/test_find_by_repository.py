async def test_find_user_by_email(user_repository, user):
    found_user = await user_repository.find_by(email=user.email)
    assert found_user is not None
    assert found_user.id == user.id
    assert found_user.email == user.email


async def test_find_user_by_email_not_found(user_repository, faker):
    not_found_user = await user_repository.find_by(email=faker.email())
    assert not_found_user is None
