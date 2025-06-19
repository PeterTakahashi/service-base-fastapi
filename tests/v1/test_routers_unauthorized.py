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
        {"method": "get", "path": "/wallet-transactions"},
        {"method": "get", "path": f"/wallet-transactions/{dammy_id}"},
        {"method": "post", "path": "/payment-intents"},
        {"method": "get", "path": "/user-api-keys"},
        {"method": "get", "path": f"/user-api-keys/{dammy_id}"},
        {"method": "post", "path": "/user-api-keys"},
        {"method": "patch", "path": f"/user-api-keys/{dammy_id}"},
        {"method": "delete", "path": f"/user-api-keys/{dammy_id}"},
        {"method": "post", "path": "/user-api-keys/verify"},
    ]
    for router in routers:
        method = router["method"]
        path = router["path"]
        response = await getattr(client, method)(path)
        check_api_exception_response(
            response,
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail_code=ErrorCode.UNAUTHORIZED,
        )
