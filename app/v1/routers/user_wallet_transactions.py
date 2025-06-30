from fastapi import Depends
from app.v1.dependencies.services.user_wallet_transaction_service import (
    get_user_wallet_transaction_service,
)
from app.v1.schemas.user_wallet_transaction import (
    UserWalletTransactionRead,
    UserWalletTransactionSearchParams,
    UserWalletTransactionListRead,
)
from app.models.user_wallet import UserWallet
from app.lib.utils.convert_id import decode_id
from app.v1.dependencies.models.user_wallet.get_user_wallet_by_current_active_user import (
    get_user_wallet_by_current_active_user,
)
from app.v1.dependencies.query_params.get_user_wallet_transaction_search_params import (
    get_user_wallet_transaction_search_params,
)
from app.core.routers.auth_api_router import AuthAPIRouter

router = AuthAPIRouter(
    prefix="/user-wallet-transactions", tags=["User Wallet Transactions"]
)


@router.get(
    "",
    response_model=UserWalletTransactionListRead,
    name="user_wallet_transactions:list_user_wallet_transactions",
)
async def list_user_wallet_transactions(
    search_params: UserWalletTransactionSearchParams = Depends(
        get_user_wallet_transaction_search_params
    ),
    user_wallet: UserWallet = Depends(get_user_wallet_by_current_active_user),
    user_wallet_transaction_service=Depends(get_user_wallet_transaction_service),
):
    """
    Retrieve a list of user_wallet transactions with filtering, sorting, and pagination.
    """
    return await user_wallet_transaction_service.get_list(
        user_wallet_id=user_wallet.id,
        search_params=search_params,
    )


@router.get(
    "/{user_wallet_transaction_id}",
    response_model=UserWalletTransactionRead,
    name="user_wallet_transactions:get_user_wallet_transaction",
)
async def get_user_wallet_transaction(
    user_wallet_transaction_id: str,
    user_wallet: UserWallet = Depends(get_user_wallet_by_current_active_user),
    user_wallet_transaction_service=Depends(get_user_wallet_transaction_service),
):
    return await user_wallet_transaction_service.get(
        user_wallet_id=user_wallet.id,
        user_wallet_transaction_id=decode_id(user_wallet_transaction_id),
    )
