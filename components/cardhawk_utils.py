"""
CardHawk OS™
Common UI Utilities
"""

from decimal import Decimal


def row_value(row, key, default=None):
    """
    Supports dicts and lightweight objects.
    """
    if row is None:
        return default

    if isinstance(row, dict):
        return row.get(key, default)

    return getattr(row, key, default)


def safe_float(value):

    try:
        if value is None:
            return 0.0

        if value == "":
            return 0.0

        return float(value)

    except Exception:

        return 0.0


def money(value):

    return f"${safe_float(value):,.2f}"


def percent(value):

    return f"{safe_float(value):.2f}%"


def integer(value):

    return f"{int(safe_float(value)):,}"


def yes_no(value):

    return "Yes" if bool(value) else "No"


def decimal(value, places=2):

    return round(Decimal(str(safe_float(value))), places)
