from fastapi import Depends, Request, status
from app.v1.schemas.payment_intent import (
    PaymentIntentCreate,
    PaymentIntentCreateResponse,
)
from app.v1.dependencies.services.organization_payment_intent_service import (
    get_organization_payment_intent_service,
)
from app.models.organization import Organization
from app.v1.services.organization_payment_intent_service import (
    OrganizationPaymentIntentService,
)
from app.v1.dependencies.models.organization.get_organization_by_id import (
    get_organization_with_address_by_id,
)

from app.core.routers.auth_api_router import AuthAPIRouter

router = AuthAPIRouter(
    prefix="/organizations/{organization_id}/payment-intents", tags=["Payment Intents"]
)


@router.post(
    "",
    response_model=PaymentIntentCreateResponse,
    name="organization::payment_intents:create_payment_intent",
    status_code=status.HTTP_201_CREATED,
)
async def create_payment_intent(
    request: Request,
    payment_intent_create: PaymentIntentCreate,
    organization: Organization = Depends(get_organization_with_address_by_id),
    service: OrganizationPaymentIntentService = Depends(
        get_organization_payment_intent_service
    ),
):
    payment_intent = await service.create_payment_intent(
        organization=organization, payment_intent_create=payment_intent_create
    )
    return payment_intent
