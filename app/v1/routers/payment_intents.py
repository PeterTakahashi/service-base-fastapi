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
