async def test_update_payment_intent_by_webhook_service(
    payment_intent_service, user_wallet, user_wallet_transaction, user_wallet_repository
):
    old_user_wallet_balance = user_wallet.balance
    # Act
    result = await payment_intent_service.update_payment_intent_by_webhook(
        stripe_payment_intent_id=user_wallet_transaction.stripe_payment_intent_id,
        currency="usd",
    )

    # Assert
    assert result is None  # The method does not return anything

    updated_user_wallet = await user_wallet_repository.find(user_wallet.id)
    assert updated_user_wallet is not None
    assert updated_user_wallet.id == user_wallet_transaction.user_wallet_id
    assert updated_user_wallet.balance == (
        old_user_wallet_balance + user_wallet_transaction.amount
    )
    assert updated_user_wallet.stripe_customer_id == user_wallet.stripe_customer_id
