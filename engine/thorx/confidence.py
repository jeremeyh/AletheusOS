def confidence_score(inputs: dict) -> float:
    return min(max(inputs.get("score", 50) / 100, 0.10), 0.98)
