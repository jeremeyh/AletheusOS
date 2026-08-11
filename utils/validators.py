def require_text(value: str, field_name: str):
    if not str(value or "").strip():
        raise ValueError(f"{field_name} is required.")
    return str(value).strip()


def safe_float(value, default: float = 0.0) -> float:
    try:
        return float(value or 0)
    except Exception:
        return default
