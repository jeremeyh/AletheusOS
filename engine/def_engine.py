def decide(score: float, confidence: float) -> str:
    if score >= 85 and confidence >= 0.70:
        return "BUY"
    if score >= 65:
        return "WATCH"
    return "PASS"
