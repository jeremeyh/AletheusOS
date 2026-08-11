def project(asset: dict, score: float) -> dict:
    current = float(asset.get("current_value") or asset.get("purchase_price") or 0)
    multiplier = 1 + (score / 100)
    return {
        "floor": round(current * 0.70, 2),
        "expected": round(current * multiplier, 2),
        "ceiling": round(current * multiplier * 3, 2),
    }
