from app.lib.utils.int_to_numeric import int_to_numeric
from app.models.enums.wallet_transaction import (
    WalletTransactionStatus,
)


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
        self, stripe_payment_intent_id: str, amount: int
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
            raise ValueError(
                "UserWallet or OrganizationWallet transaction not found for the given payment intent ID"
            )
        wallet = await wallet_repository.find(wallet_id)
        # Convert from smallest currency unit and format as Decimal with scale=9
        converted_amount = int_to_numeric(amount)
        new_balance = wallet.balance + converted_amount
        await wallet_transaction_repository.update(
            id=wallet_transaction.id,
            amount=converted_amount,  # Convert back to original amount
            balance_after_transaction=new_balance,
            wallet_transaction_status=WalletTransactionStatus.COMPLETED,
        )
        await wallet_repository.update(id=wallet.id, balance=new_balance)
        return None
