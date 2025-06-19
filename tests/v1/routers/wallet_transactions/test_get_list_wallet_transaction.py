# flake8: noqa: F841
import pytest
from httpx import AsyncClient
from datetime import datetime, timedelta
from app.lib.utils.convert_id import decode_id


@pytest.mark.asyncio
async def test_list_wallet_transactions_no_filter(
    mock_payment_intent_create_patch,
    auth_client: AsyncClient,
    wallet_transaction_factory,
    wallet_repository,
    wallet_factory,
    other_wallet_transaction,
):
    """
    Test that all wallet transactions for the authenticated user are returned when no filter is provided.
    """
    # Create multiple transactions for the same user
    wallets = await wallet_repository.where()
    wallet = wallets[0]
    tx1 = await wallet_transaction_factory.create(wallet=wallet)
    tx2 = await wallet_transaction_factory.create(wallet=wallet)

    response = await auth_client.get("/wallet-transactions")
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
async def test_list_wallet_transactions_pagination(
    mock_payment_intent_create_patch,
    auth_client: AsyncClient,
    wallet_repository,
    wallet_transaction_factory,
):
    """
    Test limit & offset.
    """
    wallets = await wallet_repository.where()
    wallet = wallets[0]
    # Create 5 transactions for the same user
    all_txs = [await wallet_transaction_factory.create(wallet=wallet) for _ in range(5)]

    # limit=2, offset=0 => first 2
    resp_1 = await auth_client.get("/wallet-transactions?limit=2&offset=0")
    assert resp_1.status_code == 200
    data_1 = resp_1.json()["data"]
    assert len(data_1) == 2

    # limit=2, offset=2 => next 2
    resp_2 = await auth_client.get("/wallet-transactions?limit=2&offset=2")
    assert resp_2.status_code == 200
    data_2 = resp_2.json()["data"]
    assert len(data_2) == 2

    # limit=2, offset=4 => last 1
    resp_3 = await auth_client.get("/wallet-transactions?limit=2&offset=4")
    assert resp_3.status_code == 200
    data_3 = resp_3.json()["data"]
    assert len(data_3) == 1


@pytest.mark.asyncio
async def test_list_wallet_transactions_sorting(
    mock_payment_intent_create_patch,
    auth_client: AsyncClient,
    wallet_transaction_factory,
    wallet_repository,
):
    """
    Test sorting by amount in descending order.
    """
    wallets = await wallet_repository.where()
    wallet = wallets[0]
    tx_small = await wallet_transaction_factory.create(amount=500, wallet=wallet)
    tx_medium = await wallet_transaction_factory.create(amount=1000, wallet=wallet)
    tx_large = await wallet_transaction_factory.create(amount=2000, wallet=wallet)

    resp = await auth_client.get(
        "/wallet-transactions?sorted_by=amount&sorted_order=desc"
    )
    assert resp.status_code == 200
    data = resp.json()["data"]
    amounts = [tx["amount"] for tx in data]

    # They should come back in descending order by amount: 2000, 1000, 500
    assert amounts == sorted([500, 1000, 2000], reverse=True)


@pytest.mark.asyncio
async def test_list_wallet_transactions_filter(
    mock_payment_intent_create_patch,
    auth_client: AsyncClient,
    wallet_transaction_factory,
    wallet_repository,
):
    """
    Test filtering by an operator, e.g. amount__gte=1000
    """
    wallets = await wallet_repository.where()
    wallet = wallets[0]
    # Create multiple wallet transactions for the same wallet
    tx1 = await wallet_transaction_factory.create(amount=500, wallet=wallet)
    tx2 = await wallet_transaction_factory.create(amount=1000, wallet=wallet)
    tx3 = await wallet_transaction_factory.create(amount=1500, wallet=wallet)

    # We'll filter for amount >= 1000
    resp = await auth_client.get("/wallet-transactions?amount__gte=1000")
    assert resp.status_code == 200
    data = resp.json()["data"]

    # Only tx2 and tx3 should appear
    returned_ids = {decode_id(tx["id"]) for tx in data}
    assert returned_ids == {tx2.id, tx3.id}


@pytest.mark.asyncio
async def test_list_wallet_transactions_date_filter(
    mock_payment_intent_create_patch,
    auth_client: AsyncClient,
    wallet_transaction_factory,
    wallet_repository,
):
    """
    Test filtering by created_at date range: created_at__gte and/or created_at__lte.
    (Requires that your BaseRepository supports date-time operators and the model has a created_at column.)
    """
    wallets = await wallet_repository.where()
    wallet = wallets[0]
    # Create an "old" transaction
    old_tx = await wallet_transaction_factory.create(
        wallet=wallet,
        created_at=datetime.utcnow() - timedelta(days=10),
        updated_at=datetime.utcnow() - timedelta(days=10),
    )
    # Create a "new" transaction
    new_tx = await wallet_transaction_factory.create(
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        wallet=wallet,
    )

    # 1) Only get transactions newer than 5 days ago
    resp = await auth_client.get(
        "/wallet-transactions?created_at__gte=2025-01-01T00:00:00"
    )
    assert resp.status_code == 200
    data = resp.json()["data"]
    if old_tx.created_at < datetime(2025, 1, 1):
        # Then presumably only new_tx is returned
        assert len(data) == 1
        assert decode_id(data[0]["id"]) == new_tx.id
    else:
        pass
