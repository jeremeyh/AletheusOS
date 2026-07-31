def quick_def(asset: dict, score: float) -> dict:
    return {
        "mode": "Q-DEF",
        "qualified": score >= 60,
        "summary": "Fast screen complete.",
    }
