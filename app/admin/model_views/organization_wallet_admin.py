from sqladmin import ModelView
from app.models.organization_wallet import OrganizationWallet


class OrganizationWalletAdmin(ModelView, model=OrganizationWallet):
    name = "Organization Wallet"
    name_plural = "Organization Wallets"

    icon = "fa-solid fa-wallet"

    column_list = [
        "id",
        "organization_id",
        "balance",
        "currency",
        "created_at",
        "organization",
        "organization_wallet_transactions",
    ]

    form_columns = [
        "organization_id",
        "balance",
        "currency",
    ]
