from app.v1.schemas.common.api_key.read import ApiKeyRead
from app.v1.schemas.user import UserRead
from pydantic import Field


class OrganizationApiKeyRead(ApiKeyRead):
    created_by_user: UserRead = Field(
        ..., description="User who created the organization API key."
    )
