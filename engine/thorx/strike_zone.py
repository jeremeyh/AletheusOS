def strike_zone(asset: dict, score: float) -> dict:
    purchase = float(asset.get("purchase_price") or 0)
    current = float(asset.get("current_value") or purchase or 0)
    base = current if current else purchase
    return {
        "auto_buy": round(base * 0.70, 2),
        "target_offer": round(base * 0.85, 2),
        "max_offer": round(base * 1.05 if score >= 80 else base * 0.95, 2),
        "walk_away": round(base * 1.20, 2),
    }
