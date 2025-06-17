from httpx import AsyncClient
from tests.common.check_error_response import (
    check_unauthorized_response,
    check_validation_error_response,
)


async def test_create_payment_intent_unauthenticated(client: AsyncClient):
    response = await client.post(
        "/payment-intents",
        json={"amount": 1000},
    )
    check_unauthorized_response(response, path="/payment-intents")


async def test_create_payment_intent_authenticated(
    mock_payment_intent_create_patch, auth_client: AsyncClient
):
    response = await auth_client.post(
        "/payment-intents",
        json={"amount": 1000},
    )
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["amount"] == 1000
    assert data["currency"] == "usd"
    assert "client_secret" in data
    assert data["status"] == "requires_payment_method"


async def test_create_payment_intent_invalid_amount(
    mock_payment_intent_create_patch, auth_client: AsyncClient
):
    response = await auth_client.post(
        "/payment-intents",
        json={"amount": -1000},  # Invalid amount
    )
    check_validation_error_response(
        response,
        path="/payment-intents",
        errors=[
            {
                "code": "validation_error",
                "title": "Validation Error",
                "detail": "Input should be greater than or equal to 100",
                "source": {"pointer": "#/amount"},
            }
        ],
    )
