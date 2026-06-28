from components.cardhawk_utils import row_value, safe_float


class ExitStrategyService:
    """Exit Strategy™ recommends hold/sell/grade/auction routes."""

    @staticmethod
    def recommend(asset):
        thorx = safe_float(row_value(asset, "thorx_score", 0))
        roi = 0
        cost = safe_float(row_value(asset, "purchase_price", 0))
        value = safe_float(row_value(asset, "current_value", 0))
        if cost:
            roi = ((value - cost) / cost) * 100

        if thorx >= 9.0:
            action = "Hold / Upgrade only at premium"
        elif roi >= 100:
            action = "Consider partial exit or list high"
        elif value < cost * 0.75:
            action = "Hold unless thesis broken"
        else:
            action = "Monitor"

        return {
            "action": action,
            "roi_percent": round(roi, 2),
            "target_sale_price": round(value * 1.25, 2) if value else 0,
            "notes": "Alpha 2.0 heuristic exit model.",
        }
