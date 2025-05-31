import pytest
from app.models.wallet import Wallet

@pytest.mark.asyncio
async def test_create_wallet(wallet_repository, user):
    wallet_data = {
        "user_id": user.id,
        "stripe_customer_id": "cus_1234",
        "balance": 1000
    }
    new_wallet = await wallet_repository.create(**wallet_data)

    assert new_wallet.id is not None
    assert new_wallet.user_id == wallet_data["user_id"]
    assert new_wallet.stripe_customer_id == wallet_data["stripe_customer_id"]
    assert new_wallet.balance == wallet_data["balance"]

    # Optionally verify it was actually persisted
    found_wallet = await wallet_repository.find(new_wallet.id)
    assert found_wallet is not None
    assert found_wallet.id == new_wallet.id
