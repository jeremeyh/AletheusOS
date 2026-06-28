from components.cardhawk_utils import row_value, safe_float


class PortfolioDigitalTwin:
    """Portfolio Digital Twin™ simulates portfolio changes."""

    @staticmethod
    def summarize(assets):
        value = sum(safe_float(row_value(a, "current_value", 0)) for a in assets or [])
        cost = sum(safe_float(row_value(a, "purchase_price", 0)) for a in assets or [])
        return {
            "asset_count": len(assets or []),
            "portfolio_value": value,
            "cost_basis": cost,
            "gain_loss": value - cost,
        }

    @staticmethod
    def simulate_add(assets, candidate_price, estimated_value):
        before = PortfolioDigitalTwin.summarize(assets)
        after = before.copy()
        after["asset_count"] += 1
        after["cost_basis"] += float(candidate_price or 0)
        after["portfolio_value"] += float(estimated_value or 0)
        after["gain_loss"] = after["portfolio_value"] - after["cost_basis"]
        return {"before": before, "after": after, "impact": {
            "value_change": after["portfolio_value"] - before["portfolio_value"],
            "cost_change": after["cost_basis"] - before["cost_basis"],
            "gain_change": after["gain_loss"] - before["gain_loss"],
        }}
