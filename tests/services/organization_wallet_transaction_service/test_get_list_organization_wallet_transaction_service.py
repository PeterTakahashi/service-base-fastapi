# flake8: noqa: F841
import pytest
from app.v1.schemas.organization_wallet_transaction import (
    OrganizationWalletTransactionRead,
    OrganizationWalletTransactionSearchParams,
)
from datetime import datetime, timedelta

pytestmark = pytest.mark.asyncio


async def test_get_list_no_filter(
    organization_wallet_transaction_service,
    organization_wallet,
    other_organization_wallet_transaction,
    organization_wallet_transaction_factory,
):
    """
    Test that get_list returns all organization_wallet transactions for the organization's organization_wallet
    when no filter pointers are specified.
    """
    # Create multiple organization_wallet transactions for the same organization/organization_wallet
    tx1 = await organization_wallet_transaction_factory.create(
        organization_wallet=organization_wallet, amount=1000
    )
    tx2 = await organization_wallet_transaction_factory.create(
        organization_wallet=organization_wallet, amount=2000
    )

    # Call our service method with an empty filter
    search_params = OrganizationWalletTransactionSearchParams()
    result = await organization_wallet_transaction_service.get_list(
        organization_wallet_id=organization_wallet.id, search_params=search_params
    )
    organization_wallet_transactions = result.data

    assert result.meta.total_count == 2
    assert result.meta.limit == 100  # Default limit
    assert result.meta.offset == 0
    assert result.meta.sorted_by == "id"
    assert result.meta.sorted_order == "asc"

    # We should only see tx1, tx2 in the results, not other_organization_wallet_transaction
    assert len(organization_wallet_transactions) == 2
    amounts = {r.amount for r in organization_wallet_transactions}
    assert amounts == {1000, 2000}

    # And they should be instances of OrganizationWalletTransactionRead
    for organization_wallet_transaction in organization_wallet_transactions:
        assert isinstance(
            organization_wallet_transaction, OrganizationWalletTransactionRead
        )


async def test_get_list_with_filter_amount_gte(
    organization_wallet_transaction_service,
    organization_wallet,
    organization_wallet_transaction_factory,
):
    """
    Test that get_list can filter by amount__gte correctly.
    """
    # Create multiple organization_wallet transactions for the same organization/organization_wallet
    await organization_wallet_transaction_factory.create(
        organization_wallet=organization_wallet, amount=500
    )
    await organization_wallet_transaction_factory.create(
        organization_wallet=organization_wallet, amount=1000
    )
    await organization_wallet_transaction_factory.create(
        organization_wallet=organization_wallet, amount=1500
    )

    # We only want transactions where amount >= 1000
    search_params = OrganizationWalletTransactionSearchParams(amount__gte=1000)
    result = await organization_wallet_transaction_service.get_list(
        organization_wallet_id=organization_wallet.id, search_params=search_params
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
    organization_wallet_transaction_service,
    organization_wallet,
    organization_wallet_transaction_factory,
    faker,
):
    """
    Test filtering by created_at__gte and created_at__lte.
    """
    # Create "old" transaction
    old_date = datetime.utcnow() - timedelta(days=10)
    tx_old = await organization_wallet_transaction_factory.create(
        organization_wallet=organization_wallet,
        created_at=old_date,
        updated_at=old_date,
    )
    # Create "new" transaction
    new_date = datetime.utcnow()
    tx_new = await organization_wallet_transaction_factory.create(
        organization_wallet=organization_wallet,
        created_at=new_date,
        updated_at=new_date,
    )

    # 1) Only get transactions newer than 5 days ago
    search_params = OrganizationWalletTransactionSearchParams(
        created_at__gte=datetime.utcnow() - timedelta(days=5)
    )
    result = await organization_wallet_transaction_service.get_list(
        organization_wallet_id=organization_wallet.id, search_params=search_params
    )
    assert len(result.data) == 1
    assert result.data[0].id == tx_new.id

    # 2) Only get transactions older than 5 days ago
    search_params = OrganizationWalletTransactionSearchParams(
        created_at__lte=datetime.utcnow() - timedelta(days=5)
    )
    result = await organization_wallet_transaction_service.get_list(
        organization_wallet_id=organization_wallet.id, search_params=search_params
    )
    assert len(result.data) == 1
    assert result.data[0].id == tx_old.id


async def test_get_list_pagination(
    organization_wallet_transaction_service,
    organization_wallet,
    organization_wallet_transaction_factory,
):
    """
    Test limit/offset pagination.
    """
    # Create 5 transactions
    tx_list = []
    for i in range(5):
        tx = await organization_wallet_transaction_factory.create(
            organization_wallet=organization_wallet
        )
        tx_list.append(tx)

    # limit=2, offset=0 => first 2
    search_params = OrganizationWalletTransactionSearchParams(limit=2, offset=0)
    result = await organization_wallet_transaction_service.get_list(
        organization_wallet_id=organization_wallet.id, search_params=search_params
    )
    assert len(result.data) == 2

    # limit=2, offset=2 => next 2
    search_params = OrganizationWalletTransactionSearchParams(limit=2, offset=2)
    result = await organization_wallet_transaction_service.get_list(
        organization_wallet_id=organization_wallet.id, search_params=search_params
    )
    assert len(result.data) == 2

    # limit=2, offset=4 => last 1
    search_params = OrganizationWalletTransactionSearchParams(limit=2, offset=4)
    result = await organization_wallet_transaction_service.get_list(
        organization_wallet_id=organization_wallet.id, search_params=search_params
    )
    assert len(result.data) == 1


async def test_get_list_sorted_by_amount_desc(
    organization_wallet_transaction_service,
    organization_wallet,
    organization_wallet_transaction_factory,
):
    """
    Test that sorting by amount desc returns correct order.
    """
    tx_small = await organization_wallet_transaction_factory.create(
        organization_wallet=organization_wallet, amount=500
    )
    tx_medium = await organization_wallet_transaction_factory.create(
        organization_wallet=organization_wallet, amount=1000
    )
    tx_large = await organization_wallet_transaction_factory.create(
        organization_wallet=organization_wallet, amount=2000
    )

    search_params = OrganizationWalletTransactionSearchParams(
        sorted_by="amount", sorted_order="desc"
    )
    result = await organization_wallet_transaction_service.get_list(
        organization_wallet_id=organization_wallet.id, search_params=search_params
    )

    amounts = [r.amount for r in result.data]
    assert amounts == sorted([500, 1000, 2000], reverse=True)
