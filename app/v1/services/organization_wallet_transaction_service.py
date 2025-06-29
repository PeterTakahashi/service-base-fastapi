from app.v1.schemas.organization_wallet_transaction import (
    OrganizationWalletTransactionRead,
    OrganizationWalletTransactionSearchParams,
    OrganizationWalletTransactionListRead,
)
from app.v1.schemas.common.list.base_list_response import ListResponseMeta


class OrganizationWalletTransactionService:
    def __init__(self, organization_wallet_transaction_repository):
        self.organization_wallet_transaction_repository = (
            organization_wallet_transaction_repository
        )

    async def get_list(
        self,
        organization_wallet_id: int,
        search_params: OrganizationWalletTransactionSearchParams,
    ) -> OrganizationWalletTransactionListRead:
        """
        Retrieve a list of organization_wallet transactions with filtering, sorting, and pagination.
        """
        organization_wallet_transactions = (
            await self.organization_wallet_transaction_repository.where(
                **search_params.model_dump(exclude_none=True),
                organization_wallet_id=organization_wallet_id,
            )
        )
        total_count = await self.organization_wallet_transaction_repository.count(
            **search_params.model_dump(
                exclude_none=True,
                exclude={"limit", "offset", "sorted_by", "sorted_order"},
            ),
            organization_wallet_id=organization_wallet_id,
        )
        return OrganizationWalletTransactionListRead(
            meta=ListResponseMeta(
                total_count=total_count,
                **search_params.model_dump(exclude_none=True),
            ),
            data=[
                OrganizationWalletTransactionRead.model_validate(tx)
                for tx in organization_wallet_transactions
            ],
        )

    async def get(
        self, organization_wallet_id: int, organization_wallet_transaction_id: int
    ) -> OrganizationWalletTransactionRead:
        """
        Retrieve a organization_wallet transaction by its ID.
        """
        organization_wallet_transaction = (
            await self.organization_wallet_transaction_repository.find_by_or_raise(
                organization_wallet_id=organization_wallet_id,
                id=organization_wallet_transaction_id,
            )
        )
        return OrganizationWalletTransactionRead.model_validate(
            organization_wallet_transaction
        )
