from pydantic import BaseModel, Field, ConfigDict


class AddressRead(BaseModel):
    city: str = Field(..., description="City, district, suburb, town, or village.")
    country: str = Field(
        ..., min_length=2, max_length=2, description="ISO-3166-1 alpha-2 country code."
    )
    line1: str = Field(
        ..., description="Address line 1 (street, PO Box, company name)."
    )
    line2: str | None = Field(
        None, description="Address line 2 (apartment, suite etc.)."
    )
    postal_code: str = Field(..., description="ZIP or postal code.")
    state: str = Field(
        ...,
        description="ISO-3166-2 subdivision code (e.g. 'NY' or 'TX', *without* country prefix).",
    )

    model_config = ConfigDict(from_attributes=True)
