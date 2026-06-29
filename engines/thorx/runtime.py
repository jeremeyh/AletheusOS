from marketplace.runtime.value import MarketplaceValue

from engines.thorx.scoring.player_score import PlayerScore
from engines.thorx.scoring.scarcity_score import ScarcityScore
from engines.thorx.scoring.market_score import MarketScore
from engines.thorx.scoring.condition_score import ConditionScore
from engines.thorx.scoring.final_score import FinalScore


class ThorX:
    """
    THORᵡ Runtime™

    Tactical Heuristic Opportunity Rating

    Multi-factor investment scoring engine for CardHawk OS™.
    """

    @staticmethod
    def score(card):
        """
        Returns an explainable THORᵡ score.

        Returns:
        {
            "score": float,
            "player": int,
            "scarcity": int,
            "market": int,
            "condition": int,
            "market_data": {...}
        }
        """

        #
        # Marketplace Intelligence
        #

        market_data = MarketplaceValue.estimate(card)

        #
        # Individual scoring engines
        #

        player_score = PlayerScore.calculate(card)

        scarcity_score = ScarcityScore.calculate(card)

        market_score = MarketScore.calculate(market_data)

        condition_score = ConditionScore.calculate(card)

        #
        # Final weighted score
        #

        final_score = FinalScore.calculate(
            player_score,
            scarcity_score,
            market_score,
            condition_score,
        )

        #
        # Explainable THORᵡ result
        #

        return {
            "score": final_score,
            "player": player_score,
            "scarcity": scarcity_score,
            "market": market_score,
            "condition": condition_score,
            "market_data": market_data,
        }
