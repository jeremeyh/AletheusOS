from asset_core.repository.asset_repository import AssetRepository
from decision_engine.runtime.engine import DecisionEngine
from portfolio.digital_twin.engine import PortfolioDigitalTwin


class FalconHealth:
    """
    FALCON™ Portfolio Health 2.0
    """

    @staticmethod
    def analyze():
        portfolio = PortfolioDigitalTwin.snapshot()
        def_summary = DecisionEngine.portfolio_summary()
        assets = AssetRepository.all(include_archived=False) or []

        asset_count = len(assets)

        if asset_count == 0:
            return {
                "collection_grade": "N/A",
                "investment_quality": 0,
                "diversification": 0,
                "risk": 0,
                "liquidity": 0,
                "scarcity": 0,
                "visual_appeal": 0,
                "overall": 0,
            }

        avg_thorx = float(portfolio.get("average_thorx") or 0)
        avg_def = float(def_summary.get("average_score") or 0)

        allocation = portfolio.get("allocation_by_player", {})
        total_value = float(portfolio.get("total_value") or 0)

        diversification = 50.0

        if allocation and total_value > 0:
            largest = max(float(value or 0) for value in allocation.values())
            concentration = largest / total_value
            diversification = max(0, min(100, 100 - concentration * 100))

        liquidity_values = []
        scarcity_values = []
        visual_values = []

        for asset in assets:
            liquidity_values.append(
                float(asset.get("liquidity_score") or 0)
                or min(float(asset.get("active_listings") or 0) * 15, 90)
                or 50
            )

            scarcity_values.append(
                float(asset.get("scarcity_score") or 0)
                or (90 if asset.get("print_run") and int(asset.get("print_run") or 999) <= 25 else 65)
            )

            visual_values.append(
                float(asset.get("eye_appeal_score") or 0)
                or float(asset.get("hawk_aeye_confidence") or 0)
                or 70
            )

        liquidity = sum(liquidity_values) / len(liquidity_values)
        scarcity = sum(scarcity_values) / len(scarcity_values)
        visual = sum(visual_values) / len(visual_values)

        risk = max(0, min(100, 100 - diversification))

        overall = (
            avg_thorx * 0.22
            + avg_def * 0.25
            + diversification * 0.18
            + liquidity * 0.12
            + scarcity * 0.13
            + visual * 0.10
        )

        if overall >= 90:
            grade = "A+"
        elif overall >= 82:
            grade = "A"
        elif overall >= 74:
            grade = "B"
        elif overall >= 65:
            grade = "C"
        else:
            grade = "D"

        return {
            "collection_grade": grade,
            "investment_quality": round((avg_thorx + avg_def) / 2, 2),
            "diversification": round(diversification, 2),
            "risk": round(risk, 2),
            "liquidity": round(liquidity, 2),
            "scarcity": round(scarcity, 2),
            "visual_appeal": round(visual, 2),
            "overall": round(overall, 2),
        }
