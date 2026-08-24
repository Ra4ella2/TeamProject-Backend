from decimal import Decimal, InvalidOperation


def amount_to_cents(amount):
    try:
        decimal_amount = Decimal(str(amount))
    except (InvalidOperation, ValueError):
        return None

    if not decimal_amount.is_finite() or decimal_amount <= 0:
        return None

    cents = decimal_amount * 100

    if cents != cents.to_integral_value():
        return None

    return int(cents)
