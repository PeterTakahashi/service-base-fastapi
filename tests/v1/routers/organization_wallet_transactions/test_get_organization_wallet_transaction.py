# from httpx import AsyncClient
# from app.lib.utils.convert_id import encode_id, decode_id
# from fastapi import status
# from tests.common.check_error_response import check_api_exception_response
# from app.lib.error_code import ErrorCode


# async def test_get_organization_wallet_transaction_authenticated(
#     auth_client: AsyncClient,
#     mock_payment_intent_create_patch,
#     organization_wallet_transaction_repository,
#     organization
# ):
#     await auth_client.post(
#         "/payment-intents",
#         json={"amount": 1000},
#     )
#     organization_wallet_transactions = await organization_wallet_transaction_repository.where()
#     organization_wallet_transaction = organization_wallet_transactions[0]
#     response = await auth_client.get(
#         f"/organizations/{encode_id(organization.id)}/wallet-transactions/{encode_id(organization_wallet_transaction.id)}"
#     )
#     assert response.status_code == 200
#     assert decode_id(response.json()["id"]) == organization_wallet_transaction.id
#     assert response.json()["amount"] == str(organization_wallet_transaction.amount)


# async def test_get_organization_wallet_transaction_not_found(
#     auth_client: AsyncClient,
#     organization,
# ):
#     response = await auth_client.get(
#         f"/organizations/{encode_id(organization.id)}/wallet-transactions/{encode_id(0)}"
#     )
#     check_api_exception_response(
#         response, status_code=status.HTTP_404_NOT_FOUND, detail_code=ErrorCode.NOT_FOUND
#     )
