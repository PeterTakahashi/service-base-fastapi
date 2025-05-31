from sqlalchemy.exc import NoResultFound
import pytest


async def test_find_by_or_raise_user(user_repository, user):
    found_user = await user_repository.find_by_or_raise(email=user.email)
    assert found_user is not None
    assert found_user.id == user.id
    assert found_user.email == user.email


async def test_find_by_or_raise_user_not_found(user_repository, faker):
    with pytest.raises(NoResultFound):
        await user_repository.find_by_or_raise(
            email=faker.email()
        )  # Using a new email that does not exist
