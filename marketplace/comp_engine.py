class CompEngine:
    """Comparable sales engine."""

    @staticmethod
    def average(comps):
        prices = [c.get("price", 0) for c in comps if c.get("price") is not None]
        return sum(prices) / len(prices) if prices else 0

    @staticmethod
    def high(comps):
        return max((c.get("price", 0) for c in comps), default=0)

    @staticmethod
    def low(comps):
        return min((c.get("price", 0) for c in comps), default=0)
