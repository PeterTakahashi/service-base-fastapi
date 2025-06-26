from httpx import AsyncClient
from fastapi import status
from tests.common.check_error_response import check_api_exception_response
from app.lib.error_code import ErrorCode
from app.lib.utils.convert_id import encode_id


async def test_routers_unauthorized(
    client: AsyncClient,
):
    dammy_id = encode_id(1)  # Dummy ID for testing
    routers = [
        {"method": "get", "path": "/users/me"},
        {"method": "patch", "path": "/users/me"},
        {"method": "get", "path": "/user-wallet-transactions"},
        {"method": "get", "path": f"/user-wallet-transactions/{dammy_id}"},
        {"method": "post", "path": "/users/payment-intents"},
        {"method": "get", "path": "/user-api-keys"},
        {"method": "get", "path": f"/user-api-keys/{dammy_id}"},
        {"method": "post", "path": "/user-api-keys"},
        {"method": "patch", "path": f"/user-api-keys/{dammy_id}"},
        {"method": "delete", "path": f"/user-api-keys/{dammy_id}"},
        {"method": "post", "path": "/user-api-keys/verify"},
        {"method": "get", "path": "/organizations"},
        {"method": "get", "path": f"/organizations/{dammy_id}"},
        {"method": "post", "path": "/organizations"},
        {"method": "patch", "path": f"/organizations/{dammy_id}"},
        {"method": "delete", "path": f"/organizations/{dammy_id}"},
        {"method": "post", "path": f"/organizations/{dammy_id}/invite"},
        {"method": "patch", "path": f"/organizations/{dammy_id}/invite/accept"},
    ]
    for router in routers:
        method = router["method"]
        path = router["path"]
        print(f"Testing {method.upper()} {path}")
        response = await getattr(client, method)(path)
        check_api_exception_response(
            response,
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail_code=ErrorCode.UNAUTHORIZED,
        )
