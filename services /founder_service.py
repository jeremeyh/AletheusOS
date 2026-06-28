from engines.command_engine import CommandEngine


class FounderService:
    """
    Founder Intelligence™

    Executive briefing service.

    Answers one question:

    'What should the founder focus on today?'
    """

    def __init__(self):

        self.command = CommandEngine()

    def morning_brief(self, assets):

        dashboard = self.command.build_dashboard(assets)

        summary = dashboard["summary"]

        opportunities = dashboard["top_opportunities"]

        brief = {

            "headline": "Today's Founder Brief™",

            "portfolio_value": summary["portfolio_value"],

            "gain_loss": summary["gain_loss"],

            "total_assets": summary["total_assets"],

            "average_thorx": summary["average_thorx"],

            "strike_zone": summary["strike_zone_count"],

            "top_pick": None,

            "alerts": []

        }

        if opportunities:

            best = opportunities[0]

            brief["top_pick"] = best

            brief["alerts"].append(
                "Highest ranked opportunity identified."
            )

        if summary["strike_zone_count"] > 0:

            brief["alerts"].append(
                f"{summary['strike_zone_count']} asset(s) currently in Strike Zone™."
            )

        if summary["gain_loss"] > 0:

            brief["alerts"].append(
                "Portfolio currently positive."
            )

        else:

            brief["alerts"].append(
                "Portfolio currently below cost basis."
            )

        return brief