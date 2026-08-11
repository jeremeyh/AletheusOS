from intelligence_convergence.engines.acquisition_ai import AcquisitionAI
from intelligence_convergence.engines.decision_model import DecisionModel
from intelligence_convergence.engines.digital_twin_2 import DigitalTwin2
from intelligence_convergence.engines.exit_intelligence import ExitIntelligence


class UnifiedIntelligenceEngine:
    """
    Unified Intelligence Engine™

    Listing / Asset → Hawk A•Eye™ → Asset DNA™ → THORᵡ™ →
    Acquisition/Exit AI → Founder AI™ → Decision™.
    """

    def __init__(self, state=None):
        self.state = state or {}

    def analyze_candidate(self, candidate):
        candidate = dict(candidate or {})

        thorx_score = float(
            candidate.get("thorx_score", candidate.get("scout_score", 0)) or 0
        )
        ni_score = float(candidate.get("ni_score", 0) or 0)
        price = float(candidate.get("price", 0) or 0)

        acquisition = AcquisitionAI.evaluate(candidate)
        decision = DecisionModel.decide(
            thorx_score=thorx_score,
            ni_score=ni_score,
            price=price,
            max_bid=acquisition.get("estimated_value", 0),
        )

        return {
            "candidate": candidate,
            "acquisition": acquisition,
            "decision": decision,
            "founder_recommendation": decision["action"],
        }

    def analyze_asset_exit(self, asset):
        return ExitIntelligence.recommend(asset)

    def simulate_future(self, assets, scenario):
        return DigitalTwin2.simulate_portfolio(assets, scenario)
