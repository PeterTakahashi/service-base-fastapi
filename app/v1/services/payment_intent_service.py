from app.v1.schemas.payment_intent import (
    PaymentIntentCreate,
    PaymentIntentCreateResponse,
)
from app.lib.utils.stripe import stripe
from app.core.config import settings
from app.models.user import User
from app.models.user_wallet import UserWallet
from app.lib.utils.int_to_numeric import int_to_numeric
from app.models.user_wallet_transaction import (
    WalletTransactionStatus,
)
from decimal import Decimal


class PaymentIntentService:
    """
    Service class for handling payment intents.
    """

    def __init__(self, user_wallet_repository, user_wallet_transaction_repository):
        self.user_wallet_repository = user_wallet_repository
        self.user_wallet_transaction_repository = user_wallet_transaction_repository

    async def create_payment_intent(
        self, user: User, payment_intent_create: PaymentIntentCreate
    ) -> PaymentIntentCreateResponse:
        user_wallet = await self.user_wallet_repository.find_by_or_raise(
            user_id=user.id
        )
        payment_intent = stripe.PaymentIntent.create(
            amount=payment_intent_create.amount
            * 100,  # Convert to smallest currency unit
            currency=settings.PAYMENT_CURRENCY,
            customer=user_wallet.stripe_customer_id,
        )
        if not payment_intent or payment_intent.client_secret is None:
            raise ValueError("Failed to create payment intent")
        await self.user_wallet_transaction_repository.create(
            user_wallet_id=user_wallet.id,
            amount=payment_intent_create.amount,
            stripe_payment_intent_id=payment_intent.id,
        )

        return PaymentIntentCreateResponse(
            id=payment_intent.id,
            amount=Decimal(payment_intent_create.amount),
            currency=payment_intent.currency,
            client_secret=payment_intent.client_secret,
            status=payment_intent.status,
        )

    async def update_payment_intent_by_webhook(
        self, stripe_payment_intent_id: str, amount: int
    ) -> UserWallet:
        user_wallet_transaction = await self.user_wallet_transaction_repository.find_by(
            stripe_payment_intent_id=stripe_payment_intent_id
        )
        if not user_wallet_transaction:
            raise ValueError(
                "UserWallet transaction not found for the given payment intent ID"
            )
        # Convert from smallest currency unit and format as Decimal with scale=9
        converted_amount = int_to_numeric(amount)
        await self.user_wallet_transaction_repository.update(
            id=user_wallet_transaction.id,
            amount=converted_amount,  # Convert back to original amount
            user_wallet_transaction_status=WalletTransactionStatus.COMPLETED,
        )
        user_wallet = await self.user_wallet_repository.find(
            user_wallet_transaction.user_wallet_id
        )
        new_balance = user_wallet.balance + converted_amount
        updated_user_wallet = await self.user_wallet_repository.update(
            id=user_wallet.id, balance=new_balance
        )
        return updated_user_wallet
