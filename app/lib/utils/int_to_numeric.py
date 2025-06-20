from decimal import Decimal, ROUND_DOWN, getcontext


def int_to_numeric(value: int) -> Decimal:
    getcontext().prec = 38
    return (Decimal(value) / Decimal('100')).quantize(Decimal('1.000000000'), rounding=ROUND_DOWN)
