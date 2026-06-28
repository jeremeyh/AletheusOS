def calculate_floor(current_value: float, risk_discount: float = 0.30) -> float:
    return round(float(current_value or 0) * (1 - risk_discount), 2)
