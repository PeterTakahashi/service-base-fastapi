from fastapi import APIRouter, Depends
from app.v1.dependencies.services.wallet_transaction_service import (
    get_wallet_transaction_service,
)
from app.lib.fastapi_users.user_setup import current_active_user
from app.v1.schemas.wallet_transaction import WalletTransactionRead
from app.models.user import User
from app.lib.convert_id import decode_id

router = APIRouter()


@router.get(
    "/{wallet_transaction_id}",
    response_model=WalletTransactionRead,
)
async def get_wallet_transaction(
    wallet_transaction_id: str,
    user: User = Depends(current_active_user),
    wallet_transaction_service=Depends(get_wallet_transaction_service),
):
    return await wallet_transaction_service.get(
        user_id=user.id, wallet_transaction_id=decode_id(wallet_transaction_id)
    )
