class LiquidityScorer:
    """Liquidity™ scoring based on brand strength, asset type, grade, and player relevance."""

    PREMIUM_BRANDS = {
        "Prizm",
        "Optic",
        "Select",
        "National Treasures",
        "Flawless",
        "Immaculate",
        "Topps Chrome",
        "Bowman Chrome",
        "Phoenix",
        "Mosaic",
        "Obsidian",
    }

    @staticmethod
    def score(asset):
        score = 5.0

        if getattr(asset, "brand", "") in LiquidityScorer.PREMIUM_BRANDS:
            score += 1.6
        if getattr(asset, "rookie", False):
            score += 0.9
        if getattr(asset, "autograph", False):
            score += 0.8
        if getattr(asset, "memorabilia", False):
            score += 0.4

        grade = str(getattr(asset, "grade", "") or "").upper()
        if "10" in grade:
            score += 1.0
        elif "9" in grade:
            score += 0.5

        return max(0.0, min(round(score, 2), 10.0))
