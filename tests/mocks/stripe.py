import pytest
from unittest.mock import patch, MagicMock
from faker import Faker
import stripe

fake = Faker()


def mock_payment_intent_create(**params):
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
        "app.v1.services.user_payment_intent_service.stripe.PaymentIntent.create",
        side_effect=mock_payment_intent_create,
    ):
        yield mock_payment_intent_create


@pytest.fixture(autouse=True)
def mock_stripe_customer_create():
    def mock_create(**params):
        assert "name" in params
        assert "email" in params

        mock_customer = MagicMock()
        mock_customer.id = f"cus_test_{params['email']}"
        return mock_customer

    patch_path = "app.lib.fastapi_users.user_manager.stripe.Customer.create"

    with patch(patch_path, side_effect=mock_create) as mock_func:
        yield mock_func


@pytest.fixture(autouse=True)
def mock_stripe_customer_modify():
    def mock_create(**params):
        assert "name" in params
        assert "email" in params

        mock_customer = MagicMock()
        mock_customer.id = f"cus_test_{params['email']}"
        return mock_customer

    patch_path = "app.lib.fastapi_users.user_manager.stripe.Customer.modify"

    with patch(patch_path, side_effect=mock_create) as mock_func:
        yield mock_func


@pytest.fixture(autouse=True)
def mock_stripe_tax_calculation_create():
    def _fake_calc_create(**params):
        mock_calc = {
            "amount_total": params["line_items"][0][
                "amount"
            ],  # Convert to smallest currency unit
            "currency": "usd",
            "customer": None,
            "customer_details": {
                "address": {
                    "city": "Seattle",
                    "country": "US",
                    "line1": "920 5th Ave",
                    "line2": "Apt 100",
                    "postal_code": "98104",
                    "state": "WA",
                },
                "address_source": "shipping",
                "ip_address": None,
                "tax_ids": [],
                "taxability_override": "none",
            },
            "expires_at": 1758634284,
            "id": "taxcalc_1RdtQ8C1hs6oFImMg9vdFNBr",
            "livemode": False,
            "object": "tax.calculation",
            "ship_from_details": None,
            "shipping_cost": None,
            "tax_amount_exclusive": 0,
            "tax_amount_inclusive": 0,
            "tax_breakdown": [
                {
                    "amount": 0,
                    "inclusive": True,
                    "tax_rate_details": {
                        "country": "US",
                        "flat_amount": None,
                        "percentage_decimal": "0.0",
                        "rate_type": "percentage",
                        "state": "WA",
                        "tax_type": "sales_tax",
                    },
                    "taxability_reason": "not_collecting",
                    "taxable_amount": 0,
                }
            ],
            "tax_date": 1750858284,
        }
        return mock_calc

    with patch.object(
        stripe.tax.Calculation, "create", side_effect=_fake_calc_create
    ) as mock_func:
        yield mock_func
