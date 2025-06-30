from fastapi import Depends
from app.v1.dependencies.services.organization_wallet_transaction_service import (
    get_organization_wallet_transaction_service,
)
from app.v1.schemas.organization_wallet_transaction import (
    OrganizationWalletTransactionRead,
    OrganizationWalletTransactionSearchParams,
    OrganizationWalletTransactionListRead,
)
from app.models.organization_wallet import OrganizationWallet
from app.lib.utils.convert_id import decode_id
from app.v1.dependencies.models.organization_wallet.get_organization_wallet import (
    get_organization_wallet,
)
from app.v1.dependencies.query_params.get_organization_wallet_transaction_search_params import (
    get_organization_wallet_transaction_search_params,
)
from app.core.routers.auth_api_router import AuthAPIRouter

router = AuthAPIRouter(
    prefix="/organizations/{organization_id}/wallet-transactions",
    tags=["Organization Wallet Transactions"],
)


@router.get(
    "",
    response_model=OrganizationWalletTransactionListRead,
    name="organization_wallet_transactions:list_organization_wallet_transactions",
)
async def list_organization_wallet_transactions(
    search_params: OrganizationWalletTransactionSearchParams = Depends(
        get_organization_wallet_transaction_search_params
    ),
    organization_wallet: OrganizationWallet = Depends(get_organization_wallet),
    organization_wallet_transaction_service=Depends(
        get_organization_wallet_transaction_service
    ),
):
    """
    Retrieve a list of organization_wallet transactions with filtering, sorting, and pagination.
    """
    return await organization_wallet_transaction_service.get_list(
        organization_wallet_id=organization_wallet.id,
        search_params=search_params,
    )


@router.get(
    "/{organization_wallet_transaction_id}",
    response_model=OrganizationWalletTransactionRead,
    name="organization_wallet_transactions:get_organization_wallet_transaction",
)
async def get_organization_wallet_transaction(
    organization_wallet_transaction_id: str,
    organization_wallet: OrganizationWallet = Depends(get_organization_wallet),
    organization_wallet_transaction_service=Depends(
        get_organization_wallet_transaction_service
    ),
):
    return await organization_wallet_transaction_service.get(
        organization_wallet_id=organization_wallet.id,
        organization_wallet_transaction_id=decode_id(
            organization_wallet_transaction_id
        ),
    )
