# flake8: noqa: F841
import pytest
from httpx import AsyncClient
from datetime import datetime, timedelta
from app.lib.utils.convert_id import decode_id


@pytest.mark.asyncio
async def test_list_user_wallet_transactions_no_filter(
    mock_payment_intent_create_patch,
    auth_client: AsyncClient,
    user,
    user_wallet_transaction_factory,
    user_wallet_repository,
):
    """
    Test that all user_wallet transactions for the authenticated user are returned when no filter is provided.
    """
    # Create multiple transactions for the same user
    user_wallet = await user_wallet_repository.find_by(user_id=user.id)
    tx1 = await user_wallet_transaction_factory.create(user_wallet=user_wallet)
    tx2 = await user_wallet_transaction_factory.create(user_wallet=user_wallet)

    response = await auth_client.get("/user-wallet-transactions")
    assert response.status_code == 200

    response_json = response.json()
    data = response_json["data"]
    # We expect only tx1 and tx2
    # Sort to ensure consistent indexing
    returned_ids = sorted(decode_id(tx["id"]) for tx in data)
    expected_ids = sorted([tx1.id, tx2.id])
    assert returned_ids == expected_ids

    # Basic content check
    for tx_data in data:
        assert "id" in tx_data
        assert "amount" in tx_data
        assert "wallet_transaction_type" in tx_data
        assert "wallet_transaction_status" in tx_data


@pytest.mark.asyncio
async def test_list_user_wallet_transactions_pagination(
    mock_payment_intent_create_patch,
    auth_client: AsyncClient,
    user_wallet_repository,
    user_wallet_transaction_factory,
):
    """
    Test limit & offset.
    """
    user_wallets = await user_wallet_repository.where()
    user_wallet = user_wallets[0]
    # Create 5 transactions for the same user
    all_txs = [
        await user_wallet_transaction_factory.create(user_wallet=user_wallet)
        for _ in range(5)
    ]

    # limit=2, offset=0 => first 2
    resp_1 = await auth_client.get("/user-wallet-transactions?limit=2&offset=0")
    assert resp_1.status_code == 200
    data_1 = resp_1.json()["data"]
    assert len(data_1) == 2

    # limit=2, offset=2 => next 2
    resp_2 = await auth_client.get("/user-wallet-transactions?limit=2&offset=2")
    assert resp_2.status_code == 200
    data_2 = resp_2.json()["data"]
    assert len(data_2) == 2

    # limit=2, offset=4 => last 1
    resp_3 = await auth_client.get("/user-wallet-transactions?limit=2&offset=4")
    assert resp_3.status_code == 200
    data_3 = resp_3.json()["data"]
    assert len(data_3) == 1


@pytest.mark.asyncio
async def test_list_user_wallet_transactions_sorting(
    mock_payment_intent_create_patch,
    auth_client: AsyncClient,
    user_wallet_transaction_factory,
    user_wallet_repository,
):
    """
    Test sorting by amount in descending order.
    """
    user_wallets = await user_wallet_repository.where()
    user_wallet = user_wallets[0]
    tx_small = await user_wallet_transaction_factory.create(
        amount=500, user_wallet=user_wallet
    )
    tx_medium = await user_wallet_transaction_factory.create(
        amount=1000, user_wallet=user_wallet
    )
    tx_large = await user_wallet_transaction_factory.create(
        amount=2000, user_wallet=user_wallet
    )

    resp = await auth_client.get(
        "/user-wallet-transactions?sorted_by=amount&sorted_order=desc"
    )
    assert resp.status_code == 200
    data = resp.json()["data"]
    amounts = [tx["amount"] for tx in data]

    # They should come back in descending order by amount: 2000, 1000, 500
    assert amounts == ["2000.000000000", "1000.000000000", "500.000000000"]


@pytest.mark.asyncio
async def test_list_user_wallet_transactions_filter(
    mock_payment_intent_create_patch,
    auth_client: AsyncClient,
    user_wallet_transaction_factory,
    user_wallet_repository,
):
    """
    Test filtering by an operator, e.g. amount__gte=1000
    """
    user_wallets = await user_wallet_repository.where()
    user_wallet = user_wallets[0]
    # Create multiple user_wallet transactions for the same user_wallet
    tx1 = await user_wallet_transaction_factory.create(
        amount=500, user_wallet=user_wallet
    )
    tx2 = await user_wallet_transaction_factory.create(
        amount=1000, user_wallet=user_wallet
    )
    tx3 = await user_wallet_transaction_factory.create(
        amount=1500, user_wallet=user_wallet
    )

    # We'll filter for amount >= 1000
    resp = await auth_client.get("/user-wallet-transactions?amount__gte=1000")
    assert resp.status_code == 200
    data = resp.json()["data"]

    # Only tx2 and tx3 should appear
    returned_ids = {decode_id(tx["id"]) for tx in data}
    assert returned_ids == {tx2.id, tx3.id}


@pytest.mark.asyncio
async def test_list_user_wallet_transactions_date_filter(
    mock_payment_intent_create_patch,
    auth_client: AsyncClient,
    user_wallet_transaction_factory,
    user_wallet_repository,
):
    """
    Test filtering by created_at date range: created_at__gte and/or created_at__lte.
    (Requires that your BaseRepository supports date-time operators and the model has a created_at column.)
    """
    user_wallets = await user_wallet_repository.where()
    user_wallet = user_wallets[0]
    # Create an "old" transaction
    old_tx = await user_wallet_transaction_factory.create(
        user_wallet=user_wallet,
        created_at=datetime.utcnow() - timedelta(days=10),
        updated_at=datetime.utcnow() - timedelta(days=10),
    )
    # Create a "new" transaction
    new_tx = await user_wallet_transaction_factory.create(
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        user_wallet=user_wallet,
    )

    # 1) Only get transactions newer than 5 days ago
    query = f"created_at__gte={(datetime.utcnow() - timedelta(days=5)).strftime('%Y-%m-%dT%H:%M:%S')}"
    resp = await auth_client.get(f"/user-wallet-transactions?{query}")
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert len(data) == 1
    assert decode_id(data[0]["id"]) == new_tx.id
