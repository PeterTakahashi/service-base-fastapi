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
        "user_wallet_transaction_type",
        "user_wallet_transaction_status",
        "created_at",
        "updated_at",
    ]

    form_columns = [
        "user_wallet_id",
        "amount",
        "balance_after_transaction",
        "stripe_payment_intent_id",
        "user_wallet_transaction_type",
        "user_wallet_transaction_status",
    ]
