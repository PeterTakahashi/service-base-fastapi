# flake8: noqa: F841
import pytest
from app.v1.schemas.user_wallet_transaction import (
    UserWalletTransactionRead,
    UserWalletTransactionSearchParams,
)
from datetime import datetime, timedelta

pytestmark = pytest.mark.asyncio


async def test_get_list_no_filter(
    user_wallet_transaction_service,
    user_wallet,
    other_user_wallet_transaction,
    user_wallet_transaction_factory,
):
    """
    Test that get_list returns all user_wallet transactions for the user's user_wallet
    when no filter pointers are specified.
    """
    # Create multiple user_wallet transactions for the same user/user_wallet
    tx1 = await user_wallet_transaction_factory.create(
        user_wallet=user_wallet, amount=1000
    )
    tx2 = await user_wallet_transaction_factory.create(
        user_wallet=user_wallet, amount=2000
    )

    # Call our service method with an empty filter
    search_params = UserWalletTransactionSearchParams()
    result = await user_wallet_transaction_service.get_list(
        user_wallet_id=user_wallet.id, search_params=search_params
    )
    user_wallet_transactions = result.data

    assert result.meta.total_count == 2
    assert result.meta.limit == 100  # Default limit
    assert result.meta.offset == 0
    assert result.meta.sorted_by == "id"
    assert result.meta.sorted_order == "asc"

    # We should only see tx1, tx2 in the results, not other_user_wallet_transaction
    assert len(user_wallet_transactions) == 2
    amounts = {r.amount for r in user_wallet_transactions}
    assert amounts == {1000, 2000}

    # And they should be instances of UserWalletTransactionRead
    for user_wallet_transaction in user_wallet_transactions:
        assert isinstance(user_wallet_transaction, UserWalletTransactionRead)


async def test_get_list_with_filter_amount_gte(
    user_wallet_transaction_service, user_wallet, user_wallet_transaction_factory
):
    """
    Test that get_list can filter by amount__gte correctly.
    """
    # Create multiple user_wallet transactions for the same user/user_wallet
    await user_wallet_transaction_factory.create(user_wallet=user_wallet, amount=500)
    await user_wallet_transaction_factory.create(user_wallet=user_wallet, amount=1000)
    await user_wallet_transaction_factory.create(user_wallet=user_wallet, amount=1500)

    # We only want transactions where amount >= 1000
    search_params = UserWalletTransactionSearchParams(amount__gte=1000)
    result = await user_wallet_transaction_service.get_list(
        user_wallet_id=user_wallet.id, search_params=search_params
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
    user_wallet_transaction_service,
    user_wallet,
    user_wallet_transaction_factory,
    faker,
):
    """
    Test filtering by created_at__gte and created_at__lte.
    """
    # Create "old" transaction
    old_date = datetime.utcnow() - timedelta(days=10)
    tx_old = await user_wallet_transaction_factory.create(
        user_wallet=user_wallet,
        created_at=old_date,
        updated_at=old_date,
    )
    # Create "new" transaction
    new_date = datetime.utcnow()
    tx_new = await user_wallet_transaction_factory.create(
        user_wallet=user_wallet,
        created_at=new_date,
        updated_at=new_date,
    )

    # 1) Only get transactions newer than 5 days ago
    search_params = UserWalletTransactionSearchParams(
        created_at__gte=datetime.utcnow() - timedelta(days=5)
    )
    result = await user_wallet_transaction_service.get_list(
        user_wallet_id=user_wallet.id, search_params=search_params
    )
    assert len(result.data) == 1
    assert result.data[0].id == tx_new.id

    # 2) Only get transactions older than 5 days ago
    search_params = UserWalletTransactionSearchParams(
        created_at__lte=datetime.utcnow() - timedelta(days=5)
    )
    result = await user_wallet_transaction_service.get_list(
        user_wallet_id=user_wallet.id, search_params=search_params
    )
    assert len(result.data) == 1
    assert result.data[0].id == tx_old.id


async def test_get_list_pagination(
    user_wallet_transaction_service, user_wallet, user_wallet_transaction_factory
):
    """
    Test limit/offset pagination.
    """
    # Create 5 transactions
    tx_list = []
    for i in range(5):
        tx = await user_wallet_transaction_factory.create(user_wallet=user_wallet)
        tx_list.append(tx)

    # limit=2, offset=0 => first 2
    search_params = UserWalletTransactionSearchParams(limit=2, offset=0)
    result = await user_wallet_transaction_service.get_list(
        user_wallet_id=user_wallet.id, search_params=search_params
    )
    assert len(result.data) == 2

    # limit=2, offset=2 => next 2
    search_params = UserWalletTransactionSearchParams(limit=2, offset=2)
    result = await user_wallet_transaction_service.get_list(
        user_wallet_id=user_wallet.id, search_params=search_params
    )
    assert len(result.data) == 2

    # limit=2, offset=4 => last 1
    search_params = UserWalletTransactionSearchParams(limit=2, offset=4)
    result = await user_wallet_transaction_service.get_list(
        user_wallet_id=user_wallet.id, search_params=search_params
    )
    assert len(result.data) == 1


async def test_get_list_sorted_by_amount_desc(
    user_wallet_transaction_service, user_wallet, user_wallet_transaction_factory
):
    """
    Test that sorting by amount desc returns correct order.
    """
    tx_small = await user_wallet_transaction_factory.create(
        user_wallet=user_wallet, amount=500
    )
    tx_medium = await user_wallet_transaction_factory.create(
        user_wallet=user_wallet, amount=1000
    )
    tx_large = await user_wallet_transaction_factory.create(
        user_wallet=user_wallet, amount=2000
    )

    search_params = UserWalletTransactionSearchParams(
        sorted_by="amount", sorted_order="desc"
    )
    result = await user_wallet_transaction_service.get_list(
        user_wallet_id=user_wallet.id, search_params=search_params
    )

    amounts = [r.amount for r in result.data]
    assert amounts == sorted([500, 1000, 2000], reverse=True)
