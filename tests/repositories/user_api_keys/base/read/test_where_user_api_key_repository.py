async def test_where_user_api_key(user_api_key_repository, soft_deleted_user_api_key):
    result = await user_api_key_repository.where(id=soft_deleted_user_api_key.id)
    assert result == []


async def test_where_user_api_key_with_deleted(
    user_api_key_repository, soft_deleted_user_api_key
):
    result = await user_api_key_repository.where(
        id=soft_deleted_user_api_key.id, disable_default_scope=True
    )
    assert result is not None
