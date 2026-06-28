from engines.thorx_engine import ThorxEngine
from engines.dex_engine import DEXEngine


class ScoutEngine:
    """
    Scout™

    Master orchestration engine.

    Coordinates the entire CardHawk intelligence pipeline.
    """

    def __init__(self):

        self.pipeline = []

    def process_asset(self, asset):

        asset = ThorxEngine.score(asset)

        intelligence = DEXEngine.evaluate(asset)

        return {

            "asset": asset,

            "intelligence": intelligence

        }

    def process_assets(self, assets):

        processed = []

        for asset in assets:

            processed.append(

                self.process_asset(asset)

            )

        return processed