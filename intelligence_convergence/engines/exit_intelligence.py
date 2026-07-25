from components.cardhawk_utils import roi_percent, row_value, safe_float


class ExitIntelligence:
    """Exit Intelligence™ recommends hold/sell/grade/auction/consign actions."""

    @staticmethod
    def recommend(asset):
        thorx = safe_float(row_value(asset, "thorx_score", 0))
        cost = safe_float(row_value(asset, "purchase_price", 0))
        value = safe_float(row_value(asset, "current_value", 0))
        roi = roi_percent(cost, value)
        grade = str(row_value(asset, "grade", "") or "").upper()

        if thorx >= 9.0:
            action = "VAULT / HOLD"
            confidence = 0.88
        elif roi >= 150:
            action = "SELL HIGH / LIST AGGRESSIVE"
            confidence = 0.84
        elif not grade and value >= 150:
            action = "GRADE FIRST"
            confidence = 0.76
        elif roi <= -35:
            action = "HOLD OR BUNDLE"
            confidence = 0.68
        else:
            action = "MONITOR"

        return {
            "action": action,
            "confidence": confidence,
            "roi_percent": round(roi, 2),
            "target_sale_price": round(value * 1.25, 2) if value else 0,
            "rationale": [
                f"THORᵡ: {thorx:.1f}",
                f"ROI: {roi:.1f}%",
                f"Grade: {grade or 'Raw/Unknown'}",
            ],
        }
