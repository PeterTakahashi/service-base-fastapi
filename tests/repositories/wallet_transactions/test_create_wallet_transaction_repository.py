from app.models.wallet_transaction import WalletTransactionType, WalletTransactionStatus


async def test_create_wallet_transaction_success(wallet_transaction_repository, wallet):
    amount = 1000  # Amount in cents
    stripe_payment_intent_id = "test_intent_id"
    wallet_transaction_type = WalletTransactionType.DEPOSIT
    wallet_transaction_status = WalletTransactionStatus.PENDING

    transaction = await wallet_transaction_repository.create_wallet_transaction(
        wallet.id,
        amount,
        stripe_payment_intent_id,
        wallet_transaction_type,
        wallet_transaction_status,
    )

    assert transaction.wallet_id == wallet.id
    assert transaction.amount == amount
    assert transaction.stripe_payment_intent_id == stripe_payment_intent_id
    assert transaction.id is not None
    assert transaction.created_at is not None
