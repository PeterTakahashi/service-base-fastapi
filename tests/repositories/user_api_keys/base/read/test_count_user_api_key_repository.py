async def test_count_user_api_key(
    user_api_key_repository, user_api_keys, soft_deleted_user_api_key
):
    count = await user_api_key_repository.count()
    assert count == 10


async def test_count_user_api_key_with_deleted(
    user_api_key_repository, user_api_keys, soft_deleted_user_api_key
):
    count = await user_api_key_repository.count(disable_default_scope=True)
    assert count == 11
