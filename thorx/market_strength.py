class MarketStrengthScorer:
    """Market Strength™ scoring based on sport, team, card category, and premium attributes."""

    HOT_SPORTS = {"Football", "Basketball", "Baseball"}
    CORE_TEAMS = {
        "Bears", "Chicago Bears", "Bulls", "Chicago Bulls", "Rockets", "Houston Rockets",
        "Texans", "Houston Texans", "Lakers", "Los Angeles Lakers"
    }

    @staticmethod
    def score(asset):
        score = 5.0

        if getattr(asset, "sport", "") in MarketStrengthScorer.HOT_SPORTS:
            score += 1.0

        if getattr(asset, "team", "") in MarketStrengthScorer.CORE_TEAMS:
            score += 1.0

        if getattr(asset, "autograph", False):
            score += 0.8

        if getattr(asset, "memorabilia", False):
            score += 0.4

        if getattr(asset, "rookie", False):
            score += 0.8

        return max(0.0, min(round(score, 2), 10.0))
