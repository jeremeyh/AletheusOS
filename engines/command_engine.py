from engines.opportunity_engine import OpportunityEngine
from engines.allocation_engine import AllocationEngine


class CommandEngine:
    """
    CardHawk OS™

    Command Engine™

    The executive intelligence layer.

    This engine prepares all information required by the
    Command Center™ dashboard.
    """

    def __init__(self):
        pass

    def build_dashboard(self, assets):

        if assets is None:
            assets = []

        total_assets = len(assets)

        portfolio_value = sum(
            float(getattr(a, "current_value", 0) or 0)
            for a in assets
        )

        cost_basis = sum(
            (
                float(getattr(a, "purchase_price", 0) or 0)
                + float(getattr(a, "shipping_cost", 0) or 0)
                + float(getattr(a, "tax", 0) or 0)
                + float(getattr(a, "fees", 0) or 0)
            )
            for a in assets
        )

        gain_loss = portfolio_value - cost_basis

        thorx_scores = [
            float(getattr(a, "thorx_score", 0) or 0)
            for a in assets
            if float(getattr(a, "thorx_score", 0) or 0) > 0
        ]

        avg_thorx = (
            sum(thorx_scores) / len(thorx_scores)
            if thorx_scores
            else 0
        )

        strike_zone = [
            a
            for a in assets
            if getattr(a, "strike_zone", False)
        ]

        top_opportunities = OpportunityEngine.rank(assets)

        allocation = {
            "player": AllocationEngine.by_player(assets),
            "team": AllocationEngine.by_team(assets),
            "sport": AllocationEngine.by_sport(assets),
        }

        dashboard = {

            "summary": {

                "total_assets": total_assets,

                "portfolio_value": round(portfolio_value, 2),

                "cost_basis": round(cost_basis, 2),

                "gain_loss": round(gain_loss, 2),

                "average_thorx": round(avg_thorx, 2),

                "strike_zone_count": len(strike_zone)

            },

            "top_opportunities": top_opportunities[:10],

            "strike_zone": strike_zone,

            "allocation": allocation,

            "recent_assets": sorted(

                assets,

                key=lambda x: getattr(x, "asset_id", 0),

                reverse=True

            )[:10]

        }

        return dashboard

    def founder_brief(self, assets):

        dashboard = self.build_dashboard(assets)

        summary = dashboard["summary"]

        return {

            "headline": "Today's Founder Brief™",

            "portfolio_value": summary["portfolio_value"],

            "gain_loss": summary["gain_loss"],

            "total_assets": summary["total_assets"],

            "average_thorx": summary["average_thorx"],

            "strike_zone_count": summary["strike_zone_count"],

            "top_pick": (

                dashboard["top_opportunities"][0]

                if dashboard["top_opportunities"]

                else None

            )

        }