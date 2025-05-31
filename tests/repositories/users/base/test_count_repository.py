async def test_count_users(user_repository, users):
    count = await user_repository.count()
    assert count == len(users)

async def test_count_users_with_filter(user_repository, users):
    count = await user_repository.count(email=users[0].email)
    assert count == 1

async def test_count_users_with_non_existent_filter(user_repository):
    count = await user_repository.count(email="non_existent_email@example.com")
    assert count == 0
