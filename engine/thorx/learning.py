def record_outcome(asset_id: int, expected: float, actual: float) -> dict:
    return {
        "asset_id": asset_id,
        "expected": expected,
        "actual": actual,
        "delta": actual - expected,
        "recorded": False,
    }
