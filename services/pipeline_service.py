from services.intelligence_service import IntelligenceService
from services.founder_service import FounderService


class PipelineService:
    """
    CardHawk Intelligence Pipeline™

    Single entry point for all intelligence.
    """

    def __init__(self):

        self.intelligence = IntelligenceService()

        self.founder = FounderService()

    def process_portfolio(self, assets):

        ranked = self.intelligence.analyze_portfolio(assets)

        founder = self.founder.morning_brief(ranked)

        return {

            "assets": ranked,

            "founder": founder

        }

    def process_asset(self, asset):

        return self.intelligence.analyze_asset(asset)