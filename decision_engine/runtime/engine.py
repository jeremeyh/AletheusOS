from asset_core.repository.asset_repository import AssetRepository
from decision_engine.models.decision import DecisionReport
from decision_engine.runtime.ddef import DDEF
from decision_engine.runtime.explanation import ExplanationEngine
from decision_engine.runtime.qdef import QDEF
from decision_engine.runtime.ranking import RankingEngine
from decision_engine.runtime.recommendation import RecommendationEngine
from decision_engine.runtime.strike_zone import StrikeZone


class DecisionEngine:
    """
    DEF — Decision Engine Framework™

    Orchestrates Q-DEF, D-DEF, recommendation,
    strike zone, explanation, and rankings.
    """

    @staticmethod
    def evaluate(asset):
        qdef_score = QDEF.score(asset)
        ddef_score = DDEF.score(asset)

        final_score = round(
            (qdef_score * 0.4) + (ddef_score * 0.6),
            2,
        )

        recommendation = RecommendationEngine.recommend(
            final_score,
            qdef_score,
            ddef_score,
        )

        confidence = RecommendationEngine.confidence(
            qdef_score,
            ddef_score,
        )

        strike_zone = StrikeZone.stars(final_score)

        explanation = ExplanationEngine.explain(
            asset,
            qdef_score,
            ddef_score,
            recommendation,
        )

        return DecisionReport(
            asset_id=asset.get("id"),
            player=asset.get("player") or "Unknown",
            qdef_score=qdef_score,
            ddef_score=ddef_score,
            final_score=final_score,
            recommendation=recommendation,
            confidence=confidence,
            strike_zone=strike_zone,
            explanation=explanation,
        ).to_dict()

    @staticmethod
    def evaluate_all():
        assets = AssetRepository.all(include_archived=False) or []

        reports = [
            DecisionEngine.evaluate(asset)
            for asset in assets
        ]

        return RankingEngine.rank(reports)

    @staticmethod
    def portfolio_summary():
        reports = DecisionEngine.evaluate_all()

        if not reports:
            return {
                "count": 0,
                "average_score": 0,
                "top_recommendation": None,
                "strike_count": 0,
                "buy_count": 0,
                "hold_count": 0,
                "watch_count": 0,
                "pass_count": 0,
                "reports": [],
            }

        avg = sum(report["final_score"] for report in reports) / len(reports)

        return {
            "count": len(reports),
            "average_score": round(avg, 2),
            "top_recommendation": reports[0],
            "strike_count": len([r for r in reports if r["recommendation"] == "STRIKE"]),
            "buy_count": len([r for r in reports if r["recommendation"] == "BUY"]),
            "hold_count": len([r for r in reports if r["recommendation"] == "HOLD"]),
            "watch_count": len([r for r in reports if r["recommendation"] == "WATCH"]),
            "pass_count": len([r for r in reports if r["recommendation"] == "PASS"]),
            "reports": reports,
        }
