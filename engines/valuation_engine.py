class ValuationEngine:
    """CardHawk OS™ valuation helper engine."""

    @staticmethod
    def cost_basis(asset):
        return float(asset.purchase_price or 0) + float(asset.shipping_cost or 0) + float(asset.tax or 0) + float(asset.fees or 0)

    @staticmethod
    def gain_loss(asset):
        return float(asset.current_value or 0) - ValuationEngine.cost_basis(asset)

    @staticmethod
    def roi_percent(asset):
        cost = ValuationEngine.cost_basis(asset)
        if cost <= 0:
            return 0.0
        return (ValuationEngine.gain_loss(asset) / cost) * 100