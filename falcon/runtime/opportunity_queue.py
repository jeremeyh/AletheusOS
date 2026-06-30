from asset_core.repository.asset_repository import AssetRepository
from decision_engine.runtime.engine import DecisionEngine
from nest.runtime.score import NestScoringEngine


class FalconOpportunityQueue:
    """
    FALCON™ Opportunity Queue

    Ranks assets using DEF + NEST + THORᵡ.
    """

    @staticmethod
    def build(limit=25):
        assets = AssetRepository.all(include_archived=False) or []

        queue = []

        for asset in assets:
            def_report = DecisionEngine.evaluate(asset)
            nest_score = NestScoringEngine.calculate(asset)

            thorx = float(asset.get("thorx_score") or 0)

            falcon_score = (
                float(def_report.get("final_score") or 0) * 0.45
                + float(nest_score.score or 0) * 0.35
                + thorx * 0.20
            )

            queue.append(
                {
                    "asset_id": asset.get("id"),
                    "player": asset.get("player") or "Unknown",
                    "brand": asset.get("brand") or "",
                    "set_name": asset.get("set_name") or "",
                    "thorx": round(thorx, 2),
                    "def_score": def_report.get("final_score"),
                    "nest_score": nest_score.score,
                    "falcon_score": round(falcon_score, 2),
                    "recommendation": def_report.get("recommendation"),
                    "confidence": def_report.get("confidence"),
                    "strike_zone": def_report.get("strike_zone"),
                }
            )

        queue = sorted(
            queue,
            key=lambda item: item.get("falcon_score", 0),
            reverse=True,
        )

        return queue[:limit]
