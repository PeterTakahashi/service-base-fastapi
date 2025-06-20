import pytest
from unittest.mock import patch
from app.v1.schemas.payment_intent import PaymentIntentCreate
from tests.mocks.stripe import mock_payment_intent_create


@pytest.mark.asyncio
@patch(
    "app.v1.services.payment_intent_service.stripe.PaymentIntent.create",
    side_effect=mock_payment_intent_create,
)
async def test_create_payment_intent_service(
    mock_create, payment_intent_service, user, user_wallet
):
    payment_intent_data = PaymentIntentCreate(amount=1000)

    payment_intent = await payment_intent_service.create_payment_intent(
        user=user, payment_intent_create=payment_intent_data
    )

    assert payment_intent is not None
    assert payment_intent.amount == payment_intent_data.amount
    assert payment_intent.currency == "usd"
    assert payment_intent.status == "requires_payment_method"
    assert payment_intent.client_secret is not None
    user_wallet_transaction = (
        await payment_intent_service.user_wallet_transaction_repository.find_by(
            user_wallet_id=user_wallet.id,
        )
    )
    assert user_wallet_transaction is not None
    assert user_wallet_transaction.amount == payment_intent_data.amount
    assert user_wallet_transaction.stripe_payment_intent_id == payment_intent.id

    mock_create.assert_called_once_with(
        amount=1000, currency="usd", customer=user_wallet.stripe_customer_id
    )
