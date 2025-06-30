from httpx import AsyncClient
from app.lib.utils.convert_id import encode_id, decode_id
from fastapi import status
from tests.common.check_error_response import check_api_exception_response
from app.lib.error_code import ErrorCode


async def test_get_user_wallet_transaction_authenticated(
    auth_client: AsyncClient,
    mock_payment_intent_create_patch,
    user_wallet_transaction_repository,
):
    await auth_client.post(
        "/users/payment-intents",
        json={"amount": 1000},
    )
    user_wallet_transactions = await user_wallet_transaction_repository.where()
    user_wallet_transaction = user_wallet_transactions[0]
    response = await auth_client.get(
        f"/user-wallet-transactions/{encode_id(user_wallet_transaction.id)}"
    )
    assert response.status_code == 200
    assert decode_id(response.json()["id"]) == user_wallet_transaction.id
    assert response.json()["amount"] == str(user_wallet_transaction.amount)


async def test_get_user_wallet_transaction_not_found(
    auth_client: AsyncClient,
):
    response = await auth_client.get(f"/user-wallet-transactions/{encode_id(0)}")
    check_api_exception_response(
        response, status_code=status.HTTP_404_NOT_FOUND, detail_code=ErrorCode.NOT_FOUND
    )
