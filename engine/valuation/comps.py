def normalize_comps(comps: list[dict]) -> list[dict]:
    """Normalize comparable sales records."""
    return comps

def median_comp_value(comps: list[dict]) -> float:
    prices = sorted(float(c.get("price", 0) or 0) for c in comps)
    if not prices:
        return 0.0
    mid = len(prices) // 2
    return prices[mid] if len(prices) % 2 else (prices[mid - 1] + prices[mid]) / 2
