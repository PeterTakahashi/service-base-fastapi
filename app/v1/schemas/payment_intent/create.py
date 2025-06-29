from pydantic import BaseModel, Field


class PaymentIntentCreate(BaseModel):
    amount: int = Field(
        ...,
        ge=1,
        description="The amount to be charged in the smallest currency unit (USD).",
        json_schema_extra={"example": 1000},
    )
