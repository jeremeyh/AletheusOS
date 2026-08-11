from components.cardhawk_utils import money, row_value, safe_float


class DynamicFounderBrief:
    """Founder Intelligence™ brief based on portfolio, events, and opportunities."""

    @staticmethod
    def generate(assets=None, events=None, offers=None):
        assets = assets or []
        events = events or []
        offers = offers or []

        value = sum(safe_float(row_value(a, "current_value", 0)) for a in assets)
        cost = sum(safe_float(row_value(a, "purchase_price", 0)) for a in assets)
        gain = value - cost
        top = sorted(
            assets,
            key=lambda a: safe_float(row_value(a, "thorx_score", 0)),
            reverse=True,
        )
        strike = [a for a in assets if bool(row_value(a, "strike_zone", False))]

        alerts = [
            f"Portfolio value: {money(value)}.",
            f"Unrealized gain/loss: {money(gain)}.",
            f"{len(strike)} Strike Zone™ asset(s).",
            f"{len(events)} intelligence event(s) available.",
            f"{len(offers)} tracked offer(s).",
        ]

        if top:
            alerts.append(
                f"Highest conviction: {row_value(top[0], 'player', 'Unknown Asset')}."
            )

        return {
            "headline": "Founder Intelligence Brief™",
            "portfolio_value": value,
            "gain_loss": gain,
            "alerts": alerts,
            "top_asset": top[0] if top else None,
            "strike_zone": strike,
            "recommended_action": "Review Strike Zone™ first."
            if strike
            else "Review highest THORᵡ assets and Scout™ candidates.",
        }
