def appreciation_projection(
    current_value: float, annual_rate: float, years: float = 1.0
) -> float:
    return round(float(current_value or 0) * ((1 + annual_rate) ** years), 2)
