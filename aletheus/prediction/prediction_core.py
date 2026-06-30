from __future__ import annotations

from typing import Any, Dict, List

from aletheus.prediction.models import (
    Forecast,
    PredictiveOpportunity,
    PredictiveRecommendation,
    PredictiveRisk,
    Scenario,
)


class AletheusPredictiveIntelligence:
    def __init__(self) -> None:
        self.version = "1.7.0"
        self.forecasts: List[Forecast] = []
        self.scenarios: List[Scenario] = []
        self.risk_history: List[PredictiveRisk] = []
        self.opportunity_history: List[PredictiveOpportunity] = []
        self.recommendation_history: List[PredictiveRecommendation] = []

    def runtime_signal(self, runtime: Any) -> Dict[str, Any]:
        return runtime.commands.dispatch("runtime.health", {}).results.get("health", {})

    def forecast(self, runtime: Any, horizon: str = "next sprint") -> Forecast:
        health = self.runtime_signal(runtime)

        signals = [
            f"Runtime status: {health.get('status', 'unknown')}",
            f"Version: {health.get('version', 'unknown')}",
            f"Applications: {health.get('applications', 0)}",
            f"Online agents: {health.get('online_agents', 0)}",
            f"Active plans: {health.get('active_plans', 0)}",
            f"Memory records: {health.get('memory_records', 0)}",
            f"Semantic concepts: {health.get('semantic_concepts', 0)}",
        ]

        confidence = 0.72
        if health.get("status") == "online":
            confidence += 0.08
        if health.get("applications", 0) >= 1:
            confidence += 0.05
        if health.get("online_agents", 0) >= 6:
            confidence += 0.05
        if health.get("active_plans", 0) >= 1:
            confidence += 0.04
        if health.get("semantic_concepts", 0) >= 5:
            confidence += 0.03

        item = Forecast(
            title="Aletheus Operating Forecast",
            horizon=horizon,
            summary="Aletheus is positioned to continue expanding from unified intelligence toward predictive, learning, and autonomous execution capabilities.",
            confidence=round(min(confidence, 0.97), 2),
            signals=signals,
        )
        self.forecasts.append(item)
        return item

    def scenario(self, title: str, premise: str, runtime: Any) -> Scenario:
        health = self.runtime_signal(runtime)

        impacts = [
            "Runtime context will expand.",
            "Memory density will increase.",
            "Knowledge graph should gain additional entities.",
            "Agent orchestration will have more useful work to perform.",
        ]

        if "marketplace" in premise.lower() or "card hawk" in premise.lower():
            expected = "Card Hawk Foundation will become more valuable as marketplace, portfolio, and acquisition intelligence create richer feedback loops."
            impacts.append("Card Hawk-specific opportunity detection should improve.")
        else:
            expected = "Aletheus will gain broader operational coverage if the scenario is executed through planning, agents, and memory."

        confidence = 0.8
        if health.get("online_agents", 0) >= 6:
            confidence += 0.07
        if health.get("applications", 0) >= 1:
            confidence += 0.05

        item = Scenario(
            title=title,
            premise=premise,
            expected_outcome=expected,
            confidence=round(min(confidence, 0.96), 2),
            impacts=impacts,
        )
        self.scenarios.append(item)
        return item

    def risks(self, runtime: Any) -> List[Dict[str, Any]]:
        health = self.runtime_signal(runtime)
        items: List[PredictiveRisk] = []

        if health.get("semantic_concepts", 0) < 5:
            items.append(
                PredictiveRisk(
                    title="Semantic sparsity",
                    description="The semantic layer has too few concepts to support rich domain reasoning.",
                    severity="medium",
                    confidence=0.91,
                    mitigation="Bootstrap Card Hawk semantics and add core player, asset, service, and decision concepts.",
                )
            )

        if health.get("active_plans", 0) == 0:
            items.append(
                PredictiveRisk(
                    title="No active execution plan",
                    description="Aletheus has planning capability, but no active plan is guiding current execution.",
                    severity="medium",
                    confidence=0.88,
                    mitigation="Create an autonomous plan for the next Card Hawk Foundation milestone.",
                )
            )

        if health.get("memory_records", 0) < 10:
            items.append(
                PredictiveRisk(
                    title="Low experience corpus",
                    description="The memory system has limited historical data, reducing learning and predictive depth.",
                    severity="low",
                    confidence=0.84,
                    mitigation="Capture more decisions, briefs, plans, and orchestration outcomes.",
                )
            )

        self.risk_history.extend(items)
        return [item.to_dict() for item in items]

    def opportunities(self, runtime: Any) -> List[Dict[str, Any]]:
        health = self.runtime_signal(runtime)
        items: List[PredictiveOpportunity] = []

        items.append(
            PredictiveOpportunity(
                title="Card Hawk Foundation deep integration",
                description="Card Hawk is registered as the reference application and should now be connected more deeply to memory, semantic intelligence, planning, and agents.",
                score=0.94,
                confidence=0.92,
                next_action="Begin Card Hawk native service binding.",
            )
        )

        if health.get("online_agents", 0) >= 6:
            items.append(
                PredictiveOpportunity(
                    title="Multi-agent execution workflows",
                    description="The agent mesh is online and ready to support coordinated execution workflows.",
                    score=0.89,
                    confidence=0.88,
                    next_action="Run multi-agent orchestration against a Card Hawk integration mission.",
                )
            )

        if health.get("semantic_concepts", 0) < 5:
            items.append(
                PredictiveOpportunity(
                    title="Semantic graph enrichment",
                    description="Low semantic density means every new concept added will materially improve reasoning quality.",
                    score=0.86,
                    confidence=0.9,
                    next_action="Bootstrap Card Hawk semantic concepts.",
                )
            )

        self.opportunity_history.extend(items)
        return [item.to_dict() for item in items]

    def recommend(self, runtime: Any) -> List[Dict[str, Any]]:
        current_risks = self.risks(runtime)

        items = [
            PredictiveRecommendation(
                title="Prioritize Card Hawk native service binding",
                recommendation="Connect Asset Vault, Portfolio Engine, Marketplace Intelligence, THORᵡ, DEF, Hawk A•Eye™, and FALCON™ into the Native Application Manager.",
                priority="critical",
                expected_gain=0.32,
                confidence=0.93,
            ),
            PredictiveRecommendation(
                title="Seed semantic and knowledge layers",
                recommendation="Create graph entities and semantic assertions for Card Hawk services, players, assets, decisions, and missions.",
                priority="high",
                expected_gain=0.24,
                confidence=0.9,
            ),
        ]

        if current_risks:
            items.append(
                PredictiveRecommendation(
                    title="Reduce predictive risk",
                    recommendation="Address current predictive risks before broadening scope.",
                    priority="high",
                    expected_gain=0.18,
                    confidence=0.86,
                )
            )

        self.recommendation_history.extend(items)
        return [item.to_dict() for item in items]

    def timeline(self, runtime: Any) -> Dict[str, Any]:
        return {
            "version": self.version,
            "forecast_count": len(self.forecasts),
            "scenario_count": len(self.scenarios),
            "risk_count": len(self.risk_history),
            "opportunity_count": len(self.opportunity_history),
            "recommendation_count": len(self.recommendation_history),
            "latest_forecast": self.forecasts[-1].to_dict() if self.forecasts else None,
            "latest_scenario": self.scenarios[-1].to_dict() if self.scenarios else None,
        }

    def stats(self) -> Dict[str, Any]:
        return {
            "version": self.version,
            "forecasts": len(self.forecasts),
            "scenarios": len(self.scenarios),
            "risks": len(self.risk_history),
            "opportunities": len(self.opportunity_history),
            "recommendations": len(self.recommendation_history),
        }


prediction_core = AletheusPredictiveIntelligence()
