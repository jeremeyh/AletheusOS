class MarketScore:

    @staticmethod
    def calculate(market):

        comps = market.get("comp_count", 0)

        if comps >= 10:
            return 95

        if comps >= 5:
            return 85

        if comps >= 3:
            return 75

        return 50
