class NIEngine:
    """NI™ — Nuclear Index scoring engine."""

    @staticmethod
    def score(asset):
        score = 0

        if asset.print_run and asset.print_run <= 10:
            score += 2
        elif asset.print_run and asset.print_run <= 25:
            score += 1.5
        elif asset.print_run and asset.print_run <= 99:
            score += 1

        if asset.autograph:
            score += 1

        if asset.memorabilia:
            score += 0.75

        if asset.rookie:
            score += 1

        if asset.thorx_score >= 9.5:
            score += 1.25
        elif asset.thorx_score >= 9:
            score += 1

        return min(round(score, 2), 5)