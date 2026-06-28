class MomentumScorer:
    """Momentum™ scoring using current value vs purchase price as Alpha proxy."""

    @staticmethod
    def score(asset):
        current = float(getattr(asset, "current_value", 0) or 0)
        cost = float(getattr(asset, "purchase_price", 0) or 0)

        if cost <= 0 or current <= 0:
            return 5.0

        ratio = current / cost

        if ratio >= 5:
            return 9.5
        if ratio >= 3:
            return 8.8
        if ratio >= 2:
            return 8.0
        if ratio >= 1.5:
            return 7.2
        if ratio >= 1:
            return 6.2
        if ratio >= 0.75:
            return 5.0
        return 4.0
