from decimal import Decimal
from typing import Annotated
from pydantic import Field, PlainSerializer


Balance = Annotated[
    Decimal,
    Field(max_digits=38, decimal_places=9),
    PlainSerializer(
        lambda v: format(v.quantize(Decimal("1E-9")), "f"),
        return_type=str,
        when_used="always",
    ),
]
