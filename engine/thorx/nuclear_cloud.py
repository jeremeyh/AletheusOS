def nuclear_cloud(asset: dict, score: float) -> dict:
    current = float(asset.get("current_value") or asset.get("purchase_price") or 0)
    return {"scenario": "Elite outcome + scarcity premium + strong grade/pop profile.", "projection": round(current * (10 + score / 10), 2)}
