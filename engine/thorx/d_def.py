def deep_def(asset: dict, score: float) -> dict:
    return {
        "mode": "D-DEF",
        "qualified": score >= 75,
        "summary": "Deep evaluation staged.",
    }
