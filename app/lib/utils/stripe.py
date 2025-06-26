import stripe
from app.core.config import settings
from fastapi import Request, status
from app.lib.exception.api_exception import init_api_exception
from app.lib.error_code import ErrorCode
from decimal import Decimal
from app.v1.schemas.common.address.read import AddressRead

stripe.api_key = settings.STRIPE_API_KEY


async def get_stripe_webhook_event(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        return stripe.Webhook.construct_event(
            payload=payload,
            sig_header=sig_header,
            secret=settings.STRIPE_WEBHOOK_SECRET,
        )
    except ValueError:
        raise init_api_exception(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail_code=ErrorCode.INVALID_PAYLOAD,
        )


def tax_calculation(amount: Decimal, address: AddressRead, tax_code: str) -> Decimal:
    calc = stripe.tax.Calculation.create(
        currency=settings.PAYMENT_CURRENCY,
        customer_details={
            "address": {
                "city": address.city,
                "country": address.country,
                "line1": address.line1,
                "line2": address.line2,
                "postal_code": address.postal_code,
                "state": address.state,
            },
            "address_source": "billing",
        },
        line_items=[
            {
                "amount": amount,
                "reference": "add deposit",
                "tax_behavior": "exclusive",
                "tax_code": tax_code,
            },
        ],
    )
    return calc
