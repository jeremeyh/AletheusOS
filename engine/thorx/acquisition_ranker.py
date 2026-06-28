def rank_acquisition_candidates(candidates: list[dict]) -> list[dict]:
    """Rank candidate assets for acquisition."""
    ranked = []
    for item in candidates:
        score = float(item.get("score", 50))
        price = float(item.get("asking_price", item.get("purchase_price", 0)) or 0)
        ranked.append({**item, "rank_score": round(score - (price / 1000), 2)})
    return sorted(ranked, key=lambda x: x["rank_score"], reverse=True)
