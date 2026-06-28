class RiskScorer:
    """Risk™ score where higher is safer."""

    RISKY_BRANDS = {"Leaf", "SAGE", "Wild Card"}

    @staticmethod
    def score(asset):
        score = 6.0

        if getattr(asset, "brand", "") in RiskScorer.RISKY_BRANDS:
            score -= 1.2

        if getattr(asset, "rookie", False):
            score -= 0.4

        pr = getattr(asset, "print_run", None)
        if pr and pr <= 25:
            score += 1.0

        if getattr(asset, "autograph", False):
            score += 0.4

        grade = str(getattr(asset, "grade", "") or "").upper()
        if "10" in grade:
            score += 0.8

        return max(0.0, min(round(score, 2), 10.0))
