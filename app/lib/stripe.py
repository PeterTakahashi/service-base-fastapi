import stripe
from app.core.config import settings
from fastapi import Request, status

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
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid signature")
