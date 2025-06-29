from sqladmin import ModelView
from app.models.user_wallet import UserWallet


class UserWalletAdmin(ModelView, model=UserWallet):
    name = "UserWallet"
    name_plural = "UserWallets"

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
