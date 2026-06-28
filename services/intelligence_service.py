from engines.scout_engine import ScoutEngine
from engines.hawk_aeye_engine import HawkAEyeEngine
from engines.genome_engine import GenomeEngine
from engines.thorx_engine import ThorxEngine
from engines.dex_engine import DEXEngine
from engines.opportunity_engine import OpportunityEngine


class IntelligenceService:
    """
    CardHawk Intelligence Pipeline™

    Orchestrates every proprietary engine.
    """

    def __init__(self):

        self.scout = ScoutEngine()

        self.hawk = HawkAEyeEngine()

        self.genome = GenomeEngine()

    def analyze_asset(self, asset):

        # THORᵡ

        asset = ThorxEngine.score(asset)

        # DEX

        dex = DEXEngine.evaluate(asset)

        # Genome

        self.genome.thorx_update(asset.thorx_score)

        self.genome.recommendation(

            dex["action"]

        )

        return {

            "asset": asset,

            "dex": dex,

            "genome": self.genome.history()

        }

    def analyze_portfolio(self, assets):

        ranked = OpportunityEngine.rank(

            assets

        )

        return ranked