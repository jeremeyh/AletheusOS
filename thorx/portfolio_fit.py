class PortfolioFitScorer:
    """Portfolio Fit™ scoring: answers whether the asset fits CardHawk specifically."""

    CORE_TEAMS = {"Bears", "Chicago Bears", "Bulls", "Chicago Bulls", "Rockets", "Houston Rockets", "Texans", "Houston Texans"}

    @staticmethod
    def score(asset):
        score = 5.0

        if getattr(asset, "team", "") in PortfolioFitScorer.CORE_TEAMS:
            score += 2.0

        if getattr(asset, "rookie", False):
            score += 1.0

        pr = getattr(asset, "print_run", None)
        if pr and pr <= 25:
            score += 1.2
        elif pr and pr <= 99:
            score += 0.6

        if getattr(asset, "autograph", False) or getattr(asset, "memorabilia", False):
            score += 0.8

        return min(round(score, 2), 10.0)
