def liquidity_score(active_count: int, sold_count: int) -> float:
    if active_count <= 0 and sold_count <= 0:
        return 0.0
    return round(min(100.0, (sold_count / max(active_count, 1)) * 50), 2)
