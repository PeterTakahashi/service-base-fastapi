from fastapi import APIRouter, Depends
from typing import List
from app.v1.dependencies.services.wallet_transaction_service import (
    get_wallet_transaction_service,
)
from app.v1.schemas.wallet_transaction import (
    WalletTransactionRead,
    WalletTransactionSearchParams,
)
from app.models.wallet import Wallet
from app.lib.convert_id import decode_id
from app.v1.dependencies.models.wallet.get_wallet_by_current_active_user import (
    get_wallet_by_current_active_user,
)

router = APIRouter()


@router.get(
    "",
    response_model=List[WalletTransactionRead],
    name="wallet_transactions:list_wallet_transactions",
)
async def list_wallet_transactions(
    search_params: WalletTransactionSearchParams = Depends(),
    wallet: Wallet = Depends(get_wallet_by_current_active_user),
    wallet_transaction_service=Depends(get_wallet_transaction_service),
):
    """
    Retrieve a list of wallet transactions with filtering, sorting, and pagination.
    """
    return await wallet_transaction_service.get_list(
        wallet_id=wallet.id,
        search_params=search_params,
    )


@router.get(
    "/{wallet_transaction_id}",
    response_model=WalletTransactionRead,
    name="wallet_transactions:get_wallet_transaction",
)
async def get_wallet_transaction(
    wallet_transaction_id: str,
    wallet: Wallet = Depends(get_wallet_by_current_active_user),
    wallet_transaction_service=Depends(get_wallet_transaction_service),
):
    return await wallet_transaction_service.get(
        wallet_id=wallet.id, wallet_transaction_id=decode_id(wallet_transaction_id)
    )
