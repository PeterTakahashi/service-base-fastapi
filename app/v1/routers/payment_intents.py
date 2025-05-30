from fastapi import APIRouter, Depends, Request, status
from app.v1.schemas.payment_intent import (
    PaymentIntentCreate,
    PaymentIntentCreateResponse,
)
from app.v1.dependencies.services.payment_intent_service import (
    get_payment_intent_service,
)
from app.lib.fastapi_users.user_setup import current_active_user
from app.models.user import User
from app.v1.services.payment_intent_service import PaymentIntentService
import json
from app.lib.stripe import get_stripe_webhook_event

router = APIRouter()


@router.post(
    "",
    response_model=PaymentIntentCreateResponse,
    name="payment_intents:create_payment_intent",
    status_code=status.HTTP_201_CREATED,
)
async def create_payment_intent(
    request: Request,
    payment_intent_create: PaymentIntentCreate,
    user: User = Depends(current_active_user),
    service: PaymentIntentService = Depends(get_payment_intent_service),
):
    payment_intent = await service.create_payment_intent(
        user=user, payment_intent_create=payment_intent_create
    )
    return payment_intent


@router.post(
    "/webhook",
    response_model=None,
    name="payment_intents:update_payment_intent_by_webhook",
    status_code=status.HTTP_200_OK,
)
async def update_payment_intent_by_webhook(
    request: Request,
    service: PaymentIntentService = Depends(get_payment_intent_service),
):
    event = await get_stripe_webhook_event(request)
    if event["type"] == "payment_intent.succeeded":
        payment_intent = event["data"]["object"]
        stripe_payment_intent_id = payment_intent["id"]
        amount = payment_intent["amount_received"]
        await service.update_payment_intent_by_webhook(
            stripe_payment_intent_id=stripe_payment_intent_id,
            amount=amount,
        )
    return None
