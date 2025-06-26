from pydantic import BaseModel, Field, ConfigDict
from app.v1.schemas.balance import Balance


class PaymentIntentCreateResponse(BaseModel):
    id: str = Field(
        ...,
        description="The unique identifier for the payment intent.",
        json_schema_extra={"example": "pi_1F8Y2e2eZvKYlo2C0d3f4g5h6"},
    )
    amount: Balance = Field(
        ...,
        description="The amount to be charged in the smallest currency unit (e.g., cents for USD).",
        json_schema_extra={"example": "10"},
    )
    amount_inclusive_tax: Balance = Field(
        ...,
        description="The amount to be charged inclusive of tax in the smallest currency unit.",
        json_schema_extra={"example": "11"},
    )
    currency: str = Field(
        ...,
        description="The currency in which the payment intent is created.",
        json_schema_extra={"example": "usd"},
    )
    client_secret: str = Field(
        ...,
        description="The client secret used to confirm the payment intent on the client side.",
        json_schema_extra={"example": "pi_1F8Y2e2eZvKYlo2C0d3f4g5h6_secret_1234567890"},
    )
    status: str = Field(
        ...,
        description="The current status of the payment intent.",
        json_schema_extra={"example": "requires_confirmation"},
    )
    model_config = ConfigDict(from_attributes=True)
