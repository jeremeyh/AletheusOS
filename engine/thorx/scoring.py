def score_asset(asset: dict) -> dict:
    score = 50
    name = str(asset.get("asset_name", "")).lower()
    serial = str(asset.get("serial_number", "")).lower()
    if "/" in serial:
        score += 12
        try:
            denom = int(serial.split("/")[-1])
            if denom <= 10:
                score += 12
            elif denom <= 25:
                score += 8
            elif denom <= 99:
                score += 4
        except Exception:
            pass
    if "auto" in name or "autograph" in name:
        score += 12
    if "rpa" in name:
        score += 16
    if "patch" in name:
        score += 8
    if "rookie" in name or "rc" in name:
        score += 8
    if "gold" in name:
        score += 6
    return {"score": min(score, 100)}
