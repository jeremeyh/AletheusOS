def risk_score(factors: dict) -> float:
    score = 0.0
    score += float(factors.get("injury", 0))
    score += float(factors.get("liquidity", 0))
    score += float(factors.get("overpay", 0))
    score += float(factors.get("population_growth", 0))
    return round(min(score, 100.0), 2)
