from engines.thorx.engine import ThorX
from founder_ai.runtime.engine import FounderAI
from hawk_aeye.runtime.service import HawkAEyeService
from marketplace.runtime.value import MarketplaceValue
from negotiation.runtime.engine import NegotiationAI


class AssetPipeline:
    """
    CardHawk Asset Intake Wizard™

    End-to-end intelligence pipeline.
    """

    @staticmethod
    def process(image_path, asking_price=0):

        #
        # Hawk A•Eye
        #

        hawk = HawkAEyeService.analyze(image_path)

        card = hawk["card"]

        #
        # Marketplace
        #

        market = MarketplaceValue.estimate(card)

        #
        # THORᵡ
        #

        thorx_score = ThorX.score(card)

        if isinstance(thorx_score, dict):
            score = thorx_score["score"]
        else:
            score = thorx_score

        #
        # Negotiation
        #

        negotiation = NegotiationAI.analyze(
            asking_price=asking_price,
            market=market,
            thorx={"score": score},
        )

        #
        # Founder AI
        #

        founder = FounderAI.brief(
            card,
            score,
            market,
        )

        return {
            "hawk": hawk,
            "market": market,
            "thorx": score,
            "negotiation": negotiation,
            "founder": founder,
        }