class VisualAppealScorer:
    """Visual Appeal™ Alpha heuristic."""

    PREMIUM_PARALLELS = [
        "Gold",
        "Black",
        "Color Blast",
        "Kaboom",
        "Downtown",
        "Manga",
        "Galactic",
        "Superfractor",
        "Pandora",
    ]

    @staticmethod
    def score(asset):
        score = 6.0
        parallel = str(getattr(asset, "parallel", "") or "")

        for term in VisualAppealScorer.PREMIUM_PARALLELS:
            if term.lower() in parallel.lower():
                score += 2.0
                break

        if getattr(asset, "memorabilia", False):
            score += 0.8

        if getattr(asset, "autograph", False):
            score += 0.5

        return min(round(score, 2), 10.0)
