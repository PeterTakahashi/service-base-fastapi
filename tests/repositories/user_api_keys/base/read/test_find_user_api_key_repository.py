from sqlalchemy.exc import NoResultFound
import pytest


async def test_find_user_api_key_repository(
    user_api_key_repository, user_api_keys, soft_deleted_user_api_key
):
    with pytest.raises(NoResultFound):
        await user_api_key_repository.find(id=soft_deleted_user_api_key.id)


async def test_find_user_api_key_repository_with_deleted(
    user_api_key_repository, user_api_keys, soft_deleted_user_api_key
):
    result = await user_api_key_repository.find(
        id=soft_deleted_user_api_key.id, disable_default_scope=True
    )
    assert result is not None
    assert result.id == soft_deleted_user_api_key.id
