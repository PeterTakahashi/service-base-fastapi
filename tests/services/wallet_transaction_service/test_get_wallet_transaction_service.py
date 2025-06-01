from app.v1.schemas.wallet_transaction import WalletTransactionRead
import pytest
from sqlalchemy.exc import NoResultFound


async def test_get_wallet_transaction(
    wallet_transaction_service, wallet, wallet_transaction
):
    fetched_wallet_transaction = await wallet_transaction_service.get(
        wallet_id=wallet.id, wallet_transaction_id=wallet_transaction.id
    )
    assert isinstance(fetched_wallet_transaction, WalletTransactionRead)
    assert fetched_wallet_transaction.id == wallet_transaction.id


async def test_get_wallet_transaction_not_found(wallet_transaction_service):
    with pytest.raises(NoResultFound):
        await wallet_transaction_service.get(wallet_id=0, wallet_transaction_id=0)
