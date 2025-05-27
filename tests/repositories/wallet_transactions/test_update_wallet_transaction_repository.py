from app.models.wallet_transaction import (
    WalletTransactionStatus,
    WalletTransactionType
)

async def test_update_wallet_transaction_success(
    wallet_transaction_repository, wallet_transaction
):
    # Arrange
    new_amount = 2000
    new_status = WalletTransactionStatus.COMPLETED

    # Act
    updated_wallet_transaction = await wallet_transaction_repository.update_wallet_transaction(
        wallet_transaction=wallet_transaction,
        amount=new_amount,
        status=new_status,
    )

    # Assert
    assert updated_wallet_transaction.amount == new_amount
    assert updated_wallet_transaction.wallet_transaction_status == new_status
    assert updated_wallet_transaction.wallet_transaction_type == wallet_transaction.wallet_transaction_type