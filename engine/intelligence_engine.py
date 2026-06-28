def quick_def_score(asset: dict) -> dict:
    score = 50
    serial = str(asset.get("serial_number", ""))
    if "/" in serial:
        score += 15
    if "auto" in str(asset.get("asset_name", "")).lower():
        score += 15
    if "rpa" in str(asset.get("asset_name", "")).lower():
        score += 20

    score = min(score, 100)

    return {
        "score": score,
        "recommendation": "BUY" if score >= 80 else "WATCH" if score >= 60 else "PASS",
    }
