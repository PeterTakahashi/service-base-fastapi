from sqladmin import ModelView
from app.models.organization_wallet_transaction import OrganizationWalletTransaction


class OrganizationWalletTransactionAdmin(
    ModelView, model=OrganizationWalletTransaction
):
    name = "Organization Wallet Transaction"
    name_plural = "Organization Wallet Transactions"

    icon = "fa-solid fa-money-bill-transfer"

    column_list = [
        "id",
        "organization_wallet_id",
        "transaction_type",
        "amount",
        "currency",
        "created_at",
        "organization_wallet",
    ]

    form_columns = [
        "organization_wallet_id",
        "transaction_type",
        "amount",
        "currency",
    ]
