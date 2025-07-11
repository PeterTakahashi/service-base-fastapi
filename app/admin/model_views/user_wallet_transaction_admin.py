from sqladmin import ModelView
from app.models.user_wallet_transaction import UserWalletTransaction


class UserWalletTransactionAdmin(ModelView, model=UserWalletTransaction):
    name = "UserWalletTransaction"
    name_plural = "UserWalletTransactions"

    icon = "fa-solid fa-money-bill-transfer"

    column_list = [
        "id",
        "user_wallet_id",
        "amount",
        "balance_after_transaction",
        "stripe_payment_intent_id",
        "wallet_transaction_type",
        "wallet_transaction_status",
        "created_at",
        "updated_at",
        "user_wallet",
    ]

    form_columns = [
        "user_wallet_id",
        "amount",
        "balance_after_transaction",
        "stripe_payment_intent_id",
        "wallet_transaction_type",
        "wallet_transaction_status",
    ]
