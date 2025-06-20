import pytest


@pytest.mark.asyncio
async def test_create_user_wallet(user_wallet_repository, user):
    user_wallet_data = {
        "user_id": user.id,
        "stripe_customer_id": "cus_1234",
        "balance": 1000,
    }
    new_user_wallet = await user_wallet_repository.create(**user_wallet_data)

    assert new_user_wallet.id is not None
    assert new_user_wallet.user_id == user_wallet_data["user_id"]
    assert new_user_wallet.stripe_customer_id == user_wallet_data["stripe_customer_id"]
    assert new_user_wallet.balance == user_wallet_data["balance"]

    # Optionally verify it was actually persisted
    found_user_wallet = await user_wallet_repository.find(new_user_wallet.id)
    assert found_user_wallet is not None
    assert found_user_wallet.id == new_user_wallet.id
