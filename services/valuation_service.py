class ValuationService:
    """
    CardHawk OS™ Valuation Service

    Placeholder service for floor / ceiling / cloud / nuclear projections.
    """

    @staticmethod
    def calculate_cost_basis(asset) -> float:
        return (
            float(asset["purchase_price"] or 0)
            + float(asset["shipping_cost"] or asset["shipping"] or 0)
            + float(asset["tax"] or 0)
            + float(asset["fees"] or 0)
        )

    @staticmethod
    def calculate_gain_loss(asset) -> float:
        return float(asset["current_value"] or 0) - ValuationService.calculate_cost_basis(asset)

    @staticmethod
    def calculate_roi(asset) -> float:
        cost = ValuationService.calculate_cost_basis(asset)
        if cost == 0:
            return 0
        return (ValuationService.calculate_gain_loss(asset) / cost) * 100

    @staticmethod
    def quick_projection(current_value: float, thorx_score: float = 0, ni_score: float = 0) -> dict:
        current_value = float(current_value or 0)
        thorx_score = float(thorx_score or 0)
        ni_score = float(ni_score or 0)

        multiplier = 1 + (thorx_score / 10) + (ni_score / 5)

        return {
            "floor": round(current_value * 0.65, 2),
            "ceiling": round(current_value * multiplier, 2),
            "cloud": round(current_value * multiplier * 2.5, 2),
            "nuclear": round(current_value * multiplier * 8, 2),
        }
