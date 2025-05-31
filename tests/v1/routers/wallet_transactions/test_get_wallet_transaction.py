from httpx import AsyncClient
from app.lib.convert_id import encode_id, decode_id
from tests.common.check_error_response import check_unauthorized_response


async def test_get_wallet_transaction_authenticated(
    auth_client: AsyncClient,
    mock_payment_intent_create_patch,
    wallet_transaction_repository,
):
    await auth_client.post(
        "/payment-intents",
        json={"amount": 1000},
    )
    wallet_transactions = await wallet_transaction_repository.where()
    wallet_transaction = wallet_transactions[0]
    response = await auth_client.get(
        f"/wallet-transactions/{encode_id(wallet_transaction.id)}"
    )
    assert response.status_code == 200
    assert decode_id(response.json()["id"]) == wallet_transaction.id
    assert response.json()["amount"] == wallet_transaction.amount


async def test_get_wallet_transaction_unauthenticated(
    client: AsyncClient,
):
    response = await client.get(f"/wallet-transactions/{encode_id(1)}")
    check_unauthorized_response(response)


async def test_get_wallet_transaction_not_found(
    auth_client: AsyncClient,
):
    response = await auth_client.get(f"/wallet-transactions/{encode_id(0)}")
    assert response.status_code == 404
    assert response.json() == {
        "errors": [
            {
                "status": "404",
                "code": "not_found",
                "title": "Not Found",
                "detail": "The requested resource could not be found.",
            }
        ]
    }
