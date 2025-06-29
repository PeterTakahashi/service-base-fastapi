async def test_exists_user_api_key(user_api_key_repository, soft_deleted_user_api_key):
    exists = await user_api_key_repository.exists()
    assert not exists


async def test_exists_user_api_key_with_deleted(
    user_api_key_repository, soft_deleted_user_api_key
):
    exists = await user_api_key_repository.exists(disable_default_scope=True)
    assert exists


async def test_exists_user_api_key_with_active_key(
    user_api_key_repository, user_api_key
):
    exists = await user_api_key_repository.exists()
    assert exists


async def test_exists_user_api_key_with_no_keys(user_api_key_repository):
    exists = await user_api_key_repository.exists()
    assert not exists


async def test_exists_user_api_key_with_multiple_keys(
    user_api_key_repository, user_api_key, soft_deleted_user_api_key
):
    exists = await user_api_key_repository.exists()
    assert exists
