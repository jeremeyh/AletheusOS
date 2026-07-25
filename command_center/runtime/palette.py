from asset_core.runtime.enrichment import AssetEnrichmentEngine
from portfolio.digital_twin.engine import PortfolioDigitalTwin


class CommandPalette:
    """
    CardHawk Command Palette™

    Global command dispatcher.
    """

    @staticmethod
    def execute(command: str):

        command = command.strip().lower()

        #
        # Refresh Portfolio
        #

        if command == "refresh portfolio":

            count = AssetEnrichmentEngine.refresh_all()

            return {
                "success": True,
                "message": f"Refreshed {count} assets."
            }

        #
        # Portfolio Snapshot
        #

        if command == "portfolio":

            return PortfolioDigitalTwin.snapshot()

        #
        # Help
        #

        if command == "help":

            return {
                "commands": [

                    "portfolio",

                    "refresh portfolio",

                    "help"

                ]
            }

        return {

            "success": False,

            "message": "Unknown command."

        }
