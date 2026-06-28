def recommendation_label(score: float, confidence: float) -> str:
    """Return a THORᵡ recommendation label."""
    if score >= 90 and confidence >= 0.80:
        return "STRONG BUY"
    if score >= 80 and confidence >= 0.65:
        return "BUY"
    if score >= 65:
        return "WATCH"
    return "PASS"
