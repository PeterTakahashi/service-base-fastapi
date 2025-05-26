from pydantic import BaseModel, Field

class PaymentIntentCreate(BaseModel):
    amount: int = Field(
        ...,
        ge=100,  # Minimum amount in cents (e.g., 100 cents = $1.00)
        description="The amount to be charged in the smallest currency unit (e.g., cents for USD).",
        json_schema_extra={"example": 1000}  # Example: $10.00
    )

class PaymentIntentCreateResponse(BaseModel):
    id: str = Field(
        ...,
        description="The unique identifier for the payment intent.",
        json_schema_extra={"example": "pi_1F8Y2e2eZvKYlo2C0d3f4g5h6"},
    )
    amount: int = Field(
        ...,
        description="The amount to be charged in the smallest currency unit (e.g., cents for USD).",
        json_schema_extra={"example": 1000}  # Example: $10.00
    )
    currency: str = Field(
        ...,
        description="The currency in which the payment intent is created.",
        json_schema_extra={"example": "usd"}
    )
    client_secret: str = Field(
        ...,
        description="The client secret used to confirm the payment intent on the client side.",
        json_schema_extra={"example": "pi_1F8Y2e2eZvKYlo2C0d3f4g5h6_secret_1234567890"}
    )
    status: str = Field(
        ...,
        description="The current status of the payment intent.",
        json_schema_extra={"example": "requires_confirmation"}
    )