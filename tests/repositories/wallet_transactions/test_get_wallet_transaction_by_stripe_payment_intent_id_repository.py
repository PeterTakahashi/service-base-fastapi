

async def test_get_wallet_transaction_by_stripe_payment_intent_id_success(
    wallet_transaction_repository, wallet, wallet_transaction
):
    # Fetch the transaction by stripe payment intent id
    fetched_transaction = await wallet_transaction_repository.get_wallet_transaction_by_stripe_payment_intent_id(
        wallet_transaction.stripe_payment_intent_id
    )

    assert fetched_transaction is not None
    assert fetched_transaction.id == wallet_transaction.id
    assert fetched_transaction.wallet_id == wallet.id
    assert fetched_transaction.amount == wallet_transaction.amount
    assert (
        fetched_transaction.stripe_payment_intent_id
        == wallet_transaction.stripe_payment_intent_id
    )
