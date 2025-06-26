from app.v1.schemas.payment_intent import (
    PaymentIntentCreate,
    PaymentIntentCreateResponse,
)
from app.lib.utils.stripe import stripe
from app.core.config import settings
from app.models.organization import Organization
from decimal import Decimal


class OrganizationPaymentIntentService:
    """
    Service class for handling payment intents.
    """

    def __init__(
        self, organization_wallet_repository, organization_wallet_transaction_repository
    ):
        self.organization_wallet_repository = organization_wallet_repository
        self.organization_wallet_transaction_repository = (
            organization_wallet_transaction_repository
        )

    async def create_payment_intent(
        self, organization: Organization, payment_intent_create: PaymentIntentCreate
    ) -> PaymentIntentCreateResponse:
        organization_wallet = (
            await self.organization_wallet_repository.find_by_or_raise(
                organization_id=organization.id
            )
        )
        payment_intent = stripe.PaymentIntent.create(
            amount=(payment_intent_create.amount * 100),
            currency=settings.PAYMENT_CURRENCY,
            customer=organization_wallet.stripe_customer_id,
        )
        if not payment_intent or payment_intent.client_secret is None:
            raise ValueError("Failed to create payment intent")
        await self.organization_wallet_transaction_repository.create(
            organization_wallet_id=organization_wallet.id,
            amount=payment_intent_create.amount,
            stripe_payment_intent_id=payment_intent.id,
        )

        return PaymentIntentCreateResponse(
            id=payment_intent.id,
            amount=Decimal(payment_intent_create.amount),
            amount_inclusive_tax=Decimal(payment_intent_create.amount),  # TODO: change
            currency=payment_intent.currency,
            client_secret=payment_intent.client_secret,
            status=payment_intent.status,
        )
