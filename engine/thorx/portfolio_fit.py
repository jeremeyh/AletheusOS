def score_portfolio_fit(asset: dict, portfolio_context: dict | None = None) -> dict:
    """Estimate how well an asset fits the current Card Hawk portfolio."""
    portfolio_context = portfolio_context or {}
    return {
        "score": 75,
        "fit": "Strong",
        "reason": "Portfolio fit placeholder based on player, scarcity, category, and allocation."
    }
