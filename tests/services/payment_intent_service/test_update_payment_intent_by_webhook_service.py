

async def test_update_payment_intent_by_webhook_service(
    payment_intent_service, wallet, wallet_transaction
):
    old_wallet_balance = wallet.balance
    # Act
    updated_wallet = await payment_intent_service.update_payment_intent_by_webhook(
        stripe_payment_intent_id=wallet_transaction.stripe_payment_intent_id,
        amount=wallet_transaction.amount,
    )

    # Assert
    assert updated_wallet is not None
    assert updated_wallet.id == wallet_transaction.wallet_id
    assert updated_wallet.balance == (old_wallet_balance + wallet_transaction.amount)
    assert updated_wallet.stripe_customer_id == wallet.stripe_customer_id
