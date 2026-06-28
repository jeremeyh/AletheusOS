def calculate_ceiling(current_value: float, upside_multiple: float = 3.0) -> float:
    return round(float(current_value or 0) * upside_multiple, 2)
