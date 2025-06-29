import pytest_asyncio
from app.v1.services.organization_payment_intent_service import (
    OrganizationPaymentIntentService,
)


@pytest_asyncio.fixture
async def organization_payment_intent_service(
    organization_wallet_repository,
    organization_wallet_transaction_repository,
    organization_address_repository,
):
    return OrganizationPaymentIntentService(
        organization_wallet_repository,
        organization_wallet_transaction_repository,
        organization_address_repository,
    )
