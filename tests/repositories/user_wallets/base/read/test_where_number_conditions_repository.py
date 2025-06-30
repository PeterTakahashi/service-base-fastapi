# flake8: noqa: F841
import pytest


async def create_users_and_user_wallets(user_factory, user_wallet_factory):
    user_1 = await user_factory.create()
    user_2 = await user_factory.create()
    user_3 = await user_factory.create()
    w1 = await user_wallet_factory.create(balance=50, user=user_1)
    w2 = await user_wallet_factory.create(balance=100, user=user_2)
    w3 = await user_wallet_factory.create(balance=200, user=user_3)
    return w1, w2, w3


@pytest.mark.asyncio
async def test_where_balance_gt(
    user_wallet_repository, user_factory, user_wallet_factory
):
    """
    balance__gt -> balance > value
    """
    w1, w2, w3 = await create_users_and_user_wallets(user_factory, user_wallet_factory)

    found_user_wallets = await user_wallet_repository.where(balance__gt=100)
    # balance が 100より大きいものは w3 のみ
    assert len(found_user_wallets) == 1
    assert found_user_wallets[0].id == w3.id
    assert found_user_wallets[0].balance == 200


@pytest.mark.asyncio
async def test_where_balance_gte(
    user_wallet_repository, user_factory, user_wallet_factory
):
    """
    balance__gte -> balance >= value
    """
    w1, w2, w3 = await create_users_and_user_wallets(user_factory, user_wallet_factory)
    found_user_wallets = await user_wallet_repository.where(balance__gte=100)
    # balance が 100以上のものは w2, w3
    assert len(found_user_wallets) == 2
    balances = [w.balance for w in found_user_wallets]
    assert sorted(balances) == [100, 200]


@pytest.mark.asyncio
async def test_where_balance_lt(
    user_wallet_repository, user_factory, user_wallet_factory
):
    """
    balance__lt -> balance < value
    """
    w1, w2, w3 = await create_users_and_user_wallets(user_factory, user_wallet_factory)
    found_user_wallets = await user_wallet_repository.where(balance__lt=100)
    # balance が 100未満のものは w1 のみ
    assert len(found_user_wallets) == 1
    assert found_user_wallets[0].id == w1.id
    assert found_user_wallets[0].balance == 50


@pytest.mark.asyncio
async def test_where_balance_lte(
    user_wallet_repository, user_factory, user_wallet_factory
):
    """
    balance__lte -> balance <= value
    """
    w1, w2, w3 = await create_users_and_user_wallets(user_factory, user_wallet_factory)

    found_user_wallets = await user_wallet_repository.where(balance__lte=100)
    # balance が 100以下のものは w1, w2
    assert len(found_user_wallets) == 2
    balances = [w.balance for w in found_user_wallets]
    assert sorted(balances) == [50, 100]


@pytest.mark.asyncio
async def test_where_balance_in(
    user_wallet_repository, user_factory, user_wallet_factory
):
    """
    balance__in -> balance IN (value1, value2, ...)
    """
    w1, w2, w3 = await create_users_and_user_wallets(user_factory, user_wallet_factory)
    found_user_wallets = await user_wallet_repository.where(balance__in=[100, 200])
    # balance が 100 または 200 のものは w2, w3
    assert len(found_user_wallets) == 2
    balances = set([w.balance for w in found_user_wallets])
    assert balances == {100, 200}
