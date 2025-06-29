import pytest
from sqlalchemy.exc import NoResultFound
from uuid import uuid4


@pytest.mark.asyncio
async def test_update_user(user_repository, user):
    """
    Test that updating a single user by id modifies the correct fields.
    """
    new_email = "updated_email@example.com"
    updated_user = await user_repository.update(user.id, email=new_email)

    assert updated_user.id == user.id
    assert updated_user.email == new_email

    # Double-check by fetching again
    found_user = await user_repository.find(user.id)
    assert found_user.email == new_email


@pytest.mark.asyncio
async def test_update_user_not_found(user_repository):
    """
    Test that updating a non-existent user raises NoResultFound.
    """
    non_existent_id = uuid4()
    with pytest.raises(NoResultFound):
        await user_repository.update(non_existent_id, email="doesnotexist@example.com")


@pytest.mark.asyncio
async def test_update_all_no_conditions(user_repository, users):
    """
    Test updating all records without specifying any conditions (similar to `UPDATE ...` with no WHERE).
    """
    updated_count = await user_repository.update_all({"failed_attempts": 2})
    assert updated_count == len(users)  # All users should be updated

    # Confirm all users have the new email
    for u in users:
        found_user = await user_repository.find(u.id)
        assert found_user.failed_attempts == 2


@pytest.mark.asyncio
async def test_update_all_with_conditions(user_repository, users):
    """
    Test updating records that match certain conditions.
    Here we assume some users are active and some are inactive.
    """
    # For the test, let's update only those who have a certain field set to True/False.
    # Adjust `is_active` or any other field depending on your actual model/fixtures.
    updated_count = await user_repository.update_all(
        {"failed_attempts": 3}, is_active=True
    )
    assert updated_count > 0  # Expect at least some users to be active

    # Verify that only users with is_active=True got the new email
    updated_users = await user_repository.where(failed_attempts=3)
    for u in updated_users:
        assert u.is_active is True

    # Ensure that users with is_active=False are *not* updated
    inactive_users = await user_repository.where(is_active=False)
    for iu in inactive_users:
        assert iu.failed_attempts != 3


@pytest.mark.asyncio
async def test_update_all_no_match(user_repository):
    """
    Test update_all when the WHERE clause matches zero records.
    """
    updated_count = await user_repository.update_all(
        {"failed_attempts": 4}, failed_attempts=5
    )
    assert updated_count == 0
