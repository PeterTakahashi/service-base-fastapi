from sqlalchemy.exc import NoResultFound
import pytest
from uuid import uuid4


async def test_find_user_by_id(user_repository, user):
    found_user = await user_repository.find(user.id)
    assert found_user is not None
    assert found_user.id == user.id


async def test_find_user_not_found(user_repository):
    with pytest.raises(NoResultFound):
        await user_repository.find(uuid4())  # Using a new UUID that does not exist
