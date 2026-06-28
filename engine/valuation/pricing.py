def fair_price(floor: float, expected: float, ceiling: float) -> float:
    return round((float(floor or 0) + float(expected or 0) * 2 + float(ceiling or 0)) / 4, 2)
