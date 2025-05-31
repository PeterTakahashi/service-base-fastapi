import pytest
from app.models.user import User

@pytest.mark.asyncio
async def test_create_user(user_repository):
    user_data = {
        "email": "test_create@example.com",
        "hashed_password": "hashed_password_example"
    }
    new_user = await user_repository.create(**user_data)

    assert new_user.id is not None  # Check ID was generated
    assert new_user.email == user_data["email"]
    assert new_user.hashed_password == user_data["hashed_password"]

    # Optionally verify it was actually persisted
    found_user = await user_repository.find(new_user.id)
    assert found_user is not None
    assert found_user.id == new_user.id

@pytest.mark.asyncio
async def test_create_user_with_invalid_field(user_repository):
    user_data = {
        "email": "test_invalid@example.com",
        "hashed_password": "hashed_password_example",
        "non_existent_field": "some_value"
    }
    with pytest.raises(Exception):
        await user_repository.create(**user_data)
