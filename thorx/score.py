from thorx.scarcity import ScarcityScorer
from thorx.liquidity import LiquidityScorer
from thorx.population import PopulationScorer
from thorx.momentum import MomentumScorer
from thorx.risk import RiskScorer
from thorx.market_strength import MarketStrengthScorer
from thorx.player_thesis import PlayerThesisScorer
from thorx.visual_appeal import VisualAppealScorer
from thorx.portfolio_fit import PortfolioFitScorer
from thorx.def_engine import DEFEngine
from thorx.dex_engine import DEXEngine


class ThorxScore:
    """THORᵡ™ Intelligence Engine Alpha 0.8."""

    WEIGHTS = {
        "scarcity": 0.17,
        "liquidity": 0.10,
        "population": 0.08,
        "momentum": 0.10,
        "risk": 0.08,
        "market_strength": 0.12,
        "player_thesis": 0.15,
        "visual_appeal": 0.08,
        "portfolio_fit": 0.12,
    }

    @staticmethod
    def score(asset):
        parts = {
            "scarcity": ScarcityScorer.score(asset),
            "liquidity": LiquidityScorer.score(asset),
            "population": PopulationScorer.score(asset),
            "momentum": MomentumScorer.score(asset),
            "risk": RiskScorer.score(asset),
            "market_strength": MarketStrengthScorer.score(asset),
            "player_thesis": PlayerThesisScorer.score(asset),
            "visual_appeal": VisualAppealScorer.score(asset),
            "portfolio_fit": PortfolioFitScorer.score(asset),
        }

        score = round(sum(parts[k] * ThorxScore.WEIGHTS[k] for k in parts), 2)

        ni = ThorxScore.nuclear_index(parts, asset)
        classification = DEFEngine.classification(score)
        recommendation = DEFEngine.recommendation(score, ni, parts["risk"])
        strike_zone = DEFEngine.strike_zone(score, ni, parts["market_strength"], parts["scarcity"])
        price_targets = DEXEngine.price_targets(asset, score)

        try:
            asset.thorx_score = score
            asset.ni_score = ni
            asset.classification = classification
            asset.recommendation = recommendation
            asset.strike_zone = strike_zone
        except Exception:
            pass

        return {
            "thorx_score": score,
            "ni_score": ni,
            "classification": classification,
            "recommendation": recommendation,
            "strike_zone": strike_zone,
            "components": parts,
            "price_targets": price_targets,
            "capital_strategy": DEXEngine.capital_size(score),
            "commentary": ThorxScore.commentary(score, ni, classification, recommendation),
        }

    @staticmethod
    def nuclear_index(parts, asset):
        score = 0.0

        if parts["scarcity"] >= 9.0:
            score += 1.4
        elif parts["scarcity"] >= 8.0:
            score += 1.0

        if parts["player_thesis"] >= 9.0:
            score += 1.2
        elif parts["player_thesis"] >= 8.0:
            score += 0.8

        if parts["visual_appeal"] >= 8.0:
            score += 0.8

        if parts["portfolio_fit"] >= 8.0:
            score += 0.8

        if getattr(asset, "autograph", False):
            score += 0.4

        if getattr(asset, "rookie", False):
            score += 0.4

        return min(round(score, 2), 5.0)

    @staticmethod
    def commentary(score, ni, classification, recommendation):
        return (
            f"THORᵡ computed {score:.2f} with NI {ni:.2f}. "
            f"Classification: {classification}. Recommendation: {recommendation}."
        )
