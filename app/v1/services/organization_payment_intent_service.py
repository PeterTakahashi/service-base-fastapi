from app.v1.schemas.payment_intent import (
    PaymentIntentCreate,
    PaymentIntentCreateResponse,
)
from app.lib.utils.stripe import stripe, tax_calculation
from app.core.config import settings
from app.models.organization import Organization
from decimal import Decimal
from app.v1.schemas.common.address.read import AddressRead
from fastapi import status
from app.lib.exception.api_exception import init_api_exception
from app.lib.error_code import ErrorCode

class OrganizationPaymentIntentService:
    """
    Service class for handling payment intents.
    """

    def __init__(
        self,
        organization_wallet_repository,
        organization_wallet_transaction_repository,
        organization_address_repository
    ):
        self.organization_wallet_repository = organization_wallet_repository
        self.organization_wallet_transaction_repository = (
            organization_wallet_transaction_repository
        )
        self.organization_address_repository = organization_address_repository

    async def create_payment_intent(
        self, organization: Organization, payment_intent_create: PaymentIntentCreate
    ) -> PaymentIntentCreateResponse:
        organization_wallet = await self.organization_wallet_repository.find_by_or_raise(
            organization_id=organization.id
        )
        amount_inclusive_tax = payment_intent_create.amount
        address = await self.organization_address_repository.find_by(
            organization_id=organization.id
        )
        address_read = AddressRead.model_validate(address) if address else None
        if address_read:
            calculation = tax_calculation(
                amount=payment_intent_create.amount,
                address=address_read,
                tax_code=settings.STRIPE_PERSONAL_TAX_CODE,
            )
            amount_inclusive_tax = calculation["amount_total"]
        payment_intent = stripe.PaymentIntent.create(
            amount=(amount_inclusive_tax * 100),
            currency=settings.PAYMENT_CURRENCY,
            customer=organization_wallet.stripe_customer_id,
        )
        if not payment_intent or payment_intent.client_secret is None:
            raise init_api_exception(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail_code=ErrorCode.FAILED_TO_CREATE_PAYMENT_INTENT,
            )
        await self.organization_wallet_transaction_repository.create(
            organization_wallet_id=organization_wallet.id,
            amount=payment_intent_create.amount,
            stripe_payment_intent_id=payment_intent.id,
        )

        return PaymentIntentCreateResponse(
            id=payment_intent.id,
            amount=Decimal(payment_intent_create.amount),
            amount_inclusive_tax=Decimal(amount_inclusive_tax),
            currency=payment_intent.currency,
            client_secret=payment_intent.client_secret,
            status=payment_intent.status,
        )
