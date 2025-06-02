from sqlalchemy.exc import NoResultFound
import pytest


async def test_soft_delete_soft_deleted_user_api_key_repository(
    user_api_key_repository, user_api_keys, soft_deleted_user_api_key
):
    with pytest.raises(NoResultFound):
        await user_api_key_repository.soft_delete(id=soft_deleted_user_api_key.id)


async def test_soft_delete_user_api_key_repository(
    user_api_key_repository,
    user_api_key,
):
    result = await user_api_key_repository.soft_delete(id=user_api_key.id)
    assert result is not None
    assert result.id == user_api_key.id
