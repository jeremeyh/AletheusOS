def valuation_projection(current_value: float, score: float) -> dict:
    current_value = float(current_value or 0)
    score = float(score or 0)
    return {
        "floor": round(current_value * 0.70, 2),
        "expected": round(current_value * (1 + score / 100), 2),
        "ceiling": round(current_value * (2 + score / 50), 2),
        "nuclear_cloud": round(current_value * (10 + score / 10), 2),
    }
