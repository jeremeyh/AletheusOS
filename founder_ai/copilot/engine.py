from portfolio.digital_twin.engine import PortfolioDigitalTwin
from asset_core.runtime.enrichment import AssetEnrichmentEngine


class FounderCopilot:
    """
    Founder Copilot™

    Natural-language command orchestrator.
    """

    @staticmethod
    def ask(prompt: str):

        q = prompt.lower().strip()

        #
        # Portfolio summary
        #

        if "portfolio" in q:

            snapshot = PortfolioDigitalTwin.snapshot()

            return {
                "type": "portfolio",
                "response": snapshot,
            }

        #
        # Refresh portfolio
        #

        if "refresh" in q:

            count = AssetEnrichmentEngine.refresh_all()

            return {
                "type": "refresh",
                "response": f"Refreshed {count} assets.",
            }

        #
        # Top assets
        #

        if "top" in q:

            snapshot = PortfolioDigitalTwin.snapshot()

            return {
                "type": "top_assets",
                "response": snapshot["top_assets"][:5],
            }

        return {
            "type": "unknown",
            "response": (
                "I don't understand that request yet. "
                "Founder Copilot learning continues."
            ),
        }
