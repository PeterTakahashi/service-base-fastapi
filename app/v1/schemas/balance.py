from decimal import Decimal
from typing import Annotated
from pydantic import Field

Balance = Annotated[
    Decimal,
    Field(max_digits=38, decimal_places=9)
]
