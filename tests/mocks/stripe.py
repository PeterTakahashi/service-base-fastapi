import pytest
from unittest.mock import patch, MagicMock
from faker import Faker

fake = Faker()


def mock_payment_intent_create(**kwargs):
    mock_intent = MagicMock()
    mock_intent.id = f"pi_test_{fake.uuid4()}"
    mock_intent.amount = 1000
    mock_intent.currency = "usd"
    mock_intent.client_secret = f"secret_{mock_intent.id}"
    mock_intent.status = "requires_payment_method"
    return mock_intent


@pytest.fixture
def mock_payment_intent_create_patch():
    with patch(
        "app.v1.services.payment_intent_service.stripe.PaymentIntent.create",
        side_effect=mock_payment_intent_create,
    ):
        yield mock_payment_intent_create


@pytest.fixture(autouse=True)
def mock_stripe_customer_create():
    def mock_create(**kwargs):
        assert "name" in kwargs
        assert "email" in kwargs

        mock_customer = MagicMock()
        mock_customer.id = f"cus_test_{kwargs['email']}"
        return mock_customer

    patch_path = "app.lib.fastapi_users.user_manager.stripe.Customer.create"

    with patch(patch_path, side_effect=mock_create) as mock_func:
        yield mock_func
