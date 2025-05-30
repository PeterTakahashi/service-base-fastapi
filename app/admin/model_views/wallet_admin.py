from sqladmin import ModelView
from app.models.wallet import Wallet


class WalletAdmin(ModelView, model=Wallet):
    name = "Wallet"
    name_plural = "Wallets"

    icon = "fa-solid fa-wallet"

    column_list = [
        "id",
        "user_id",
        "stripe_customer_id",
        "balance",
        "created_at",
        "updated_at",
    ]

    form_columns = [
        "user_id",
        "stripe_customer_id",
        "balance",
    ]
