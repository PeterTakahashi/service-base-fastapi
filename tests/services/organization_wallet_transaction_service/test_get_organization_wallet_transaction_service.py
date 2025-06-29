from app.v1.schemas.organization_wallet_transaction import (
    OrganizationWalletTransactionRead,
)
import pytest
from sqlalchemy.exc import NoResultFound


async def test_get_organization_wallet_transaction(
    organization_wallet_transaction_service,
    organization_wallet,
    organization_wallet_transaction,
):
    fetched_organization_wallet_transaction = (
        await organization_wallet_transaction_service.get(
            organization_wallet_id=organization_wallet.id,
            organization_wallet_transaction_id=organization_wallet_transaction.id,
        )
    )
    assert isinstance(
        fetched_organization_wallet_transaction, OrganizationWalletTransactionRead
    )
    assert (
        fetched_organization_wallet_transaction.id == organization_wallet_transaction.id
    )


async def test_get_organization_wallet_transaction_not_found(
    organization_wallet_transaction_service,
):
    with pytest.raises(NoResultFound):
        await organization_wallet_transaction_service.get(
            organization_wallet_id=0, organization_wallet_transaction_id=0
        )
