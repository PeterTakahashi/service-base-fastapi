from sqladmin import ModelView
from app.db.session import engine
from app.models.wallet_transaction import WalletTransaction

class WalletTransactionAdmin(ModelView, model=WalletTransaction):
    name = "WalletTransaction"
    name_plural = "WalletTransactions"

    icon = "fa-solid fa-money-bill-transfer"

    column_list = [
        "id",
        "wallet_id",
        "amount",
        "stripe_payment_intent_id",
        "wallet_transaction_type",
        "wallet_transaction_status",
        "created_at",
        "updated_at",
    ]

    form_columns = [
        "wallet_id",
        "amount",
        "stripe_payment_intent_id",
        "wallet_transaction_type",
        "wallet_transaction_status",
    ]