from app.models.enums.wallet_transaction import (
    WalletTransactionStatus,
)
from app.lib.exception.api_exception import init_api_exception
from app.lib.error_code import ErrorCode
from fastapi import status
from app.lib.utils.stripe import stripe
from app.lib.utils.convert_id import encode_id


class PaymentIntentService:
    """
    Service class for handling payment intents.
    """

    def __init__(
        self,
        user_wallet_repository,
        user_wallet_transaction_repository,
        organization_wallet_repository,
        organization_wallet_transaction_repository,
    ):
        self.user_wallet_repository = user_wallet_repository
        self.user_wallet_transaction_repository = user_wallet_transaction_repository
        self.organization_wallet_repository = organization_wallet_repository
        self.organization_wallet_transaction_repository = (
            organization_wallet_transaction_repository
        )

    async def update_payment_intent_by_webhook(
        self,
        stripe_payment_intent_id: str,
        currency: str,
    ) -> None:
        user_wallet_transaction = await self.user_wallet_transaction_repository.find_by(
            stripe_payment_intent_id=stripe_payment_intent_id
        )
        if user_wallet_transaction:
            wallet_transaction = user_wallet_transaction
            wallet_id = wallet_transaction.user_wallet_id
            wallet_repository = self.user_wallet_repository
            wallet_transaction_repository = self.user_wallet_transaction_repository
        organization_wallet_transaction = (
            await self.organization_wallet_transaction_repository.find_by(
                stripe_payment_intent_id=stripe_payment_intent_id
            )
        )
        if organization_wallet_transaction:
            wallet_transaction = organization_wallet_transaction
            wallet_id = wallet_transaction.organization_wallet_id
            wallet_repository = self.organization_wallet_repository
            wallet_transaction_repository = (
                self.organization_wallet_transaction_repository
            )
        if not user_wallet_transaction and not organization_wallet_transaction:
            raise init_api_exception(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail_code=ErrorCode.FAILED_TO_WEBHOOK_PAYMENT_INTENT_UPDATE,
            )
        wallet = await wallet_repository.find(wallet_id)
        new_balance = wallet.balance + wallet_transaction.amount
        await wallet_transaction_repository.update(
            id=wallet_transaction.id,
            balance_after_transaction=new_balance,
            wallet_transaction_status=WalletTransactionStatus.COMPLETED,
        )
        await wallet_repository.update(id=wallet.id, balance=new_balance)
        await self._maybe_send_invoice(
            stripe_customer_id=wallet.stripe_customer_id,
            amount=wallet_transaction.amount_inclusive_tax,
            currency=currency,
            wallet_transaction_id=wallet_transaction.id,
        )
        return None

    async def _maybe_send_invoice(
        self,
        stripe_customer_id: str,
        amount: int,
        currency: str,
        wallet_transaction_id: int,
    ) -> None:
        try:
            customer = stripe.Customer.retrieve(stripe_customer_id)
            address = customer.get("address", {})

            if not address or not address.get("line1"):
                return

            stripe.InvoiceItem.create(
                customer=customer.id,
                amount=amount,  # 最小通貨単位
                currency=currency,
                description=f"Wallet top-up ({encode_id(wallet_transaction_id)})",
            )
            stripe.Invoice.create(
                customer=customer.id,
                collection_method="send_invoice",
                days_until_due=0,
                auto_advance=True,
            )
        except Exception as e:
            print(f"Failed to send invoice: {e}")
            return None
