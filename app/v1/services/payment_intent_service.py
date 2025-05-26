from app.v1.schemas.payment_intent import PaymentIntentCreate, PaymentIntentCreateResponse
from app.lib.stripe import stripe
from app.core.config import settings
from app.models.user import User


class PaymentIntentService:
    """
    Service class for handling payment intents.
    """

    def __init__(self, wallet_repository, wallet_transaction_repository):
        self.wallet_repository = wallet_repository
        self.wallet_transaction_repository = wallet_transaction_repository

    async def create_payment_intent(
        self,
        user: User,
        payment_intent_create: PaymentIntentCreate
    ) -> PaymentIntentCreateResponse:
        wallet = await self.wallet_repository.get_wallet_by_user_id(user.id)
        payment_intent = stripe.PaymentIntent.create(
            amount=payment_intent_create.amount,
            currency=settings.PAYMENT_CURRENCY,
            customer=wallet.stripe_customer_id,
        )
        if not payment_intent:
            raise ValueError("Failed to create payment intent")
        await self.wallet_transaction_repository.create_wallet_transaction(
            wallet_id=wallet.id,
            amount=payment_intent_create.amount,
            stripe_payment_intent_id=payment_intent.id
        )

        return PaymentIntentCreateResponse(
            id=payment_intent.id,
            amount=payment_intent.amount,
            currency=payment_intent.currency,
            client_secret=payment_intent.client_secret,
            status=payment_intent.status
        )
