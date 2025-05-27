async def test_update_wallet_success(wallet_repository, user, wallet):
    # Arrange
    balance = 10000  # Initial balance in cents

    # Act
    updated_wallet = await wallet_repository.update_wallet(
        wallet=wallet,
        balance=balance,
    )

    # Assert
    assert updated_wallet is not None
    assert updated_wallet.id == wallet.id
    assert updated_wallet.user_id == user.id
    assert updated_wallet.stripe_customer_id == wallet.stripe_customer_id
    assert updated_wallet.balance == balance
