class PopulationScorer:
    """Population™ scoring. Higher means more favorable population profile."""

    @staticmethod
    def score(asset):
        pop = getattr(asset, "population", None)

        if pop is None:
            return 5.0

        try:
            pop = int(pop)
        except Exception:
            return 5.0

        if pop <= 3:
            return 9.8
        if pop <= 10:
            return 9.2
        if pop <= 25:
            return 8.4
        if pop <= 50:
            return 7.5
        if pop <= 100:
            return 6.6
        if pop <= 250:
            return 5.6
        return 4.5
