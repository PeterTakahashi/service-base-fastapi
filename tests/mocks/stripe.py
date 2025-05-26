from unittest.mock import MagicMock

def mock_payment_intent_create(**kwargs):
    mock_intent = MagicMock()
    mock_intent.id = "pi_test_123"
    mock_intent.amount = 1000
    mock_intent.currency = "usd"
    mock_intent.client_secret = "test_secret_123"
    mock_intent.status = "requires_payment_method"
    return mock_intent
