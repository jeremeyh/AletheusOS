def money(value) -> str:
    try:
        return f"${float(value):,.2f}"
    except Exception:
        return "$0.00"

def pct(value) -> str:
    try:
        return f"{float(value):.2f}%"
    except Exception:
        return "0.00%"
