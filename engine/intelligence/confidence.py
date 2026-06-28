def intelligence_confidence(source_count: int, agreement_score: float) -> float:
    return round(min(0.99, max(0.1, (source_count / 10) * agreement_score)), 3)
