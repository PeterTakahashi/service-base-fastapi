from app.v1.schemas.user_wallet_transaction import UserWalletTransactionRead
import pytest
from sqlalchemy.exc import NoResultFound


async def test_get_user_wallet_transaction(
    user_wallet_transaction_service, user_wallet, user_wallet_transaction
):
    fetched_user_wallet_transaction = await user_wallet_transaction_service.get(
        user_wallet_id=user_wallet.id,
        user_wallet_transaction_id=user_wallet_transaction.id,
    )
    assert isinstance(fetched_user_wallet_transaction, UserWalletTransactionRead)
    assert fetched_user_wallet_transaction.id == user_wallet_transaction.id


async def test_get_user_wallet_transaction_not_found(user_wallet_transaction_service):
    with pytest.raises(NoResultFound):
        await user_wallet_transaction_service.get(
            user_wallet_id=0, user_wallet_transaction_id=0
        )
