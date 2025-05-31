import pytest
from sqlalchemy.exc import NoResultFound
from uuid import uuid4


@pytest.mark.asyncio
async def test_destroy_user(user_repository, user):
    """
    Test destroying a single user by id.
    """
    # Ensure the user exists initially
    found_user = await user_repository.find(user.id)
    assert found_user is not None

    # Destroy the user
    await user_repository.destroy(user.id)

    # Now, attempting to find should raise NoResultFound
    with pytest.raises(NoResultFound):
        await user_repository.find(user.id)


@pytest.mark.asyncio
async def test_destroy_user_not_found(user_repository):
    """
    Test that destroying a non-existent user raises NoResultFound.
    """
    non_existent_id = uuid4()
    with pytest.raises(NoResultFound):
        await user_repository.destroy(non_existent_id)


@pytest.mark.asyncio
async def test_destroy_all_no_conditions(user_repository, users):
    """
    Test destroying all records when no conditions are given.
    """
    # Confirm we have users in DB
    count_before = await user_repository.count()
    assert count_before == len(users)

    # Destroy them all
    deleted_count = await user_repository.destroy_all()
    assert deleted_count == len(users)

    # Now, no users should remain
    count_after = await user_repository.count()
    assert count_after == 0


@pytest.mark.asyncio
async def test_destroy_all_with_conditions(user_repository, users):
    """
    Test destroying records matching certain conditions.
    Here we assume some users have is_active=True.
    """
    # Count how many active users there are
    active_users_count = await user_repository.count(is_active=True)
    assert (
        active_users_count > 0
    ), "There should be at least one active user in the fixtures."

    # Destroy only those who are active
    deleted_count = await user_repository.destroy_all(is_active=True)
    assert deleted_count == active_users_count

    # Confirm active users are gone
    remaining_active = await user_repository.count(is_active=True)
    assert remaining_active == 0


@pytest.mark.asyncio
async def test_destroy_all_no_match(user_repository):
    """
    Test destroy_all when the conditions match zero records.
    """
    # Use conditions that match no users
    deleted_count = await user_repository.destroy_all(
        email="this_should_not_match_any@example.com"
    )
    assert deleted_count == 0
