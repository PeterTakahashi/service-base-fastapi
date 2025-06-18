# flake8: noqa: F841
import pytest
from app.v1.schemas.wallet_transaction import (
    WalletTransactionRead,
    WalletTransactionSearchParams,
)
from datetime import datetime, timedelta

pytestmark = pytest.mark.asyncio


async def test_get_list_no_filter(
    wallet_transaction_service,
    wallet,
    other_wallet_transaction,
    wallet_transaction_factory,
):
    """
    Test that get_list returns all wallet transactions for the user's wallet
    when no filter pointers are specified.
    """
    # Create multiple wallet transactions for the same user/wallet
    tx1 = await wallet_transaction_factory.create(wallet=wallet, amount=1000)
    tx2 = await wallet_transaction_factory.create(wallet=wallet, amount=2000)

    # Call our service method with an empty filter
    search_params = WalletTransactionSearchParams()
    result = await wallet_transaction_service.get_list(
        wallet_id=wallet.id, search_params=search_params
    )
    wallet_transactions = result.data

    assert result.meta.total_count == 2
    assert result.meta.limit == 100  # Default limit
    assert result.meta.offset == 0
    assert result.meta.sorted_by == "id"
    assert result.meta.sorted_order == "asc"

    # We should only see tx1, tx2 in the results, not other_wallet_transaction
    assert len(wallet_transactions) == 2
    amounts = {r.amount for r in wallet_transactions}
    assert amounts == {1000, 2000}

    # And they should be instances of WalletTransactionRead
    for wallet_transaction in wallet_transactions:
        assert isinstance(wallet_transaction, WalletTransactionRead)


async def test_get_list_with_filter_amount_gte(
    wallet_transaction_service, wallet, wallet_transaction_factory
):
    """
    Test that get_list can filter by amount__gte correctly.
    """
    # Create multiple wallet transactions for the same user/wallet
    await wallet_transaction_factory.create(wallet=wallet, amount=500)
    await wallet_transaction_factory.create(wallet=wallet, amount=1000)
    await wallet_transaction_factory.create(wallet=wallet, amount=1500)

    # We only want transactions where amount >= 1000
    search_params = WalletTransactionSearchParams(amount__gte=1000)
    result = await wallet_transaction_service.get_list(
        wallet_id=wallet.id, search_params=search_params
    )
    assert result.meta.total_count == 2
    assert result.meta.limit == 100  # Default limit
    assert result.meta.offset == 0
    assert result.meta.sorted_by == "id"
    assert result.meta.sorted_order == "asc"
    assert len(result.data) == 2
    amounts = sorted([r.amount for r in result.data])
    assert amounts == [1000, 1500]


async def test_get_list_with_filter_created_at_range(
    wallet_transaction_service,
    wallet,
    wallet_transaction_factory,
    faker,
):
    """
    Test filtering by created_at__gte and created_at__lte.
    """
    # Create "old" transaction
    old_date = datetime.utcnow() - timedelta(days=10)
    tx_old = await wallet_transaction_factory.create(
        wallet=wallet,
        created_at=old_date,
        updated_at=old_date,
    )
    # Create "new" transaction
    new_date = datetime.utcnow()
    tx_new = await wallet_transaction_factory.create(
        wallet=wallet,
        created_at=new_date,
        updated_at=new_date,
    )

    # 1) Only get transactions newer than 5 days ago
    search_params = WalletTransactionSearchParams(
        created_at__gte=datetime.utcnow() - timedelta(days=5)
    )
    result = await wallet_transaction_service.get_list(
        wallet_id=wallet.id, search_params=search_params
    )
    assert len(result.data) == 1
    assert result.data[0].id == tx_new.id

    # 2) Only get transactions older than 5 days ago
    search_params = WalletTransactionSearchParams(
        created_at__lte=datetime.utcnow() - timedelta(days=5)
    )
    result = await wallet_transaction_service.get_list(
        wallet_id=wallet.id, search_params=search_params
    )
    assert len(result.data) == 1
    assert result.data[0].id == tx_old.id


async def test_get_list_pagination(
    wallet_transaction_service, wallet, wallet_transaction_factory
):
    """
    Test limit/offset pagination.
    """
    # Create 5 transactions
    tx_list = []
    for i in range(5):
        tx = await wallet_transaction_factory.create(wallet=wallet)
        tx_list.append(tx)

    # limit=2, offset=0 => first 2
    search_params = WalletTransactionSearchParams(limit=2, offset=0)
    result = await wallet_transaction_service.get_list(
        wallet_id=wallet.id, search_params=search_params
    )
    assert len(result.data) == 2

    # limit=2, offset=2 => next 2
    search_params = WalletTransactionSearchParams(limit=2, offset=2)
    result = await wallet_transaction_service.get_list(
        wallet_id=wallet.id, search_params=search_params
    )
    assert len(result.data) == 2

    # limit=2, offset=4 => last 1
    search_params = WalletTransactionSearchParams(limit=2, offset=4)
    result = await wallet_transaction_service.get_list(
        wallet_id=wallet.id, search_params=search_params
    )
    assert len(result.data) == 1


async def test_get_list_sorted_by_amount_desc(
    wallet_transaction_service, wallet, wallet_transaction_factory
):
    """
    Test that sorting by amount desc returns correct order.
    """
    tx_small = await wallet_transaction_factory.create(wallet=wallet, amount=500)
    tx_medium = await wallet_transaction_factory.create(wallet=wallet, amount=1000)
    tx_large = await wallet_transaction_factory.create(wallet=wallet, amount=2000)

    search_params = WalletTransactionSearchParams(
        sorted_by="amount", sorted_order="desc"
    )
    result = await wallet_transaction_service.get_list(
        wallet_id=wallet.id, search_params=search_params
    )

    amounts = [r.amount for r in result.data]
    assert amounts == sorted([500, 1000, 2000], reverse=True)
