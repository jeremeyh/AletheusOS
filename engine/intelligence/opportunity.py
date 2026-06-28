def opportunity_score(discount_pct: float, scarcity: float, liquidity: float) -> float:
    return round(min(100.0, discount_pct * 0.4 + scarcity * 0.35 + liquidity * 0.25), 2)
