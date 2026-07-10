from __future__ import annotations

from typing import Any

from aletheus.prediction.engine import (
    PredictiveIntelligenceEngine,
)
from aletheus.prediction.models import (
    Forecast,
    PredictiveOpportunity,
    PredictiveRecommendation,
    PredictiveRisk,
    Scenario,
)


class PredictionAdapter:
    """
    Stable runtime-facing prediction contract.

    This adapter isolates the command layer from the incomplete historical
    prediction compatibility modules and provides one bounded interface for
    forecast, scenario, risk, opportunity, recommendation, timeline, and
    statistics operations.
    """

    VERSION = "17.0-compat"

    def __init__(self):
        self.version = self.VERSION
        self.engine = PredictiveIntelligenceEngine()
        self._forecasts: list[Forecast] = []
        self._scenarios: list[Scenario] = []
        self._risks: list[PredictiveRisk] = []
        self._opportunities: list[PredictiveOpportunity] = []
        self._recommendations: list[
            PredictiveRecommendation
        ] = []

    @staticmethod
    def _runtime_signals(runtime: Any) -> list[str]:
        signals = [
            "Runtime command registry is operational.",
            "Aletheus bounded capability domains are active.",
        ]

        commands = getattr(runtime, "commands", None)

        if commands is not None:
            try:
                signals.append(
                    f"{commands.count()} runtime commands registered."
                )
            except Exception:
                pass

        return signals

    def forecast(
        self,
        *,
        runtime: Any,
        horizon: str = "next sprint",
    ) -> Forecast:
        command_count = 0

        try:
            command_count = runtime.commands.count()
        except Exception:
            pass

        confidence = 0.82 if command_count else 0.68

        forecast = Forecast(
            title="Aletheus Runtime Forecast",
            horizon=horizon,
            summary=(
                "Aletheus is expected to continue stabilizing through "
                "bounded adapter repair, explicit compatibility contracts, "
                "and compiled command dispatch."
            ),
            confidence=confidence,
            signals=self._runtime_signals(runtime),
        )

        self._forecasts.append(forecast)
        self.engine.create_prediction(forecast.to_dict())
        return forecast

    def scenario(
        self,
        *,
        title: str,
        premise: str,
        runtime: Any,
    ) -> Scenario:
        scenario = Scenario(
            title=title,
            premise=premise,
            expected_outcome=(
                "The capability is integrated through a bounded runtime "
                "adapter while preserving governance, observability, and "
                "command-contract compatibility."
            ),
            confidence=0.8,
            impacts=[
                "Reduced runtime-core responsibility",
                "Improved command compatibility",
                "Stronger subsystem isolation",
            ],
        )

        self._scenarios.append(scenario)
        self.engine.create_prediction(scenario.to_dict())
        return scenario

    def risks(self, runtime: Any) -> list[dict[str, Any]]:
        risks = [
            PredictiveRisk(
                title="Compatibility contract drift",
                description=(
                    "Legacy command names or result envelopes may diverge "
                    "from current capability implementations."
                ),
                severity="high",
                confidence=0.91,
                mitigation=(
                    "Maintain explicit aliases, bounded adapters, and "
                    "contract-focused regression tests."
                ),
            ),
            PredictiveRisk(
                title="Runtime composition drift",
                description=(
                    "Runtime attributes may remain bound to compatibility "
                    "modules rather than live capability instances."
                ),
                severity="medium",
                confidence=0.87,
                mitigation=(
                    "Audit composition bindings and require capability "
                    "interface validation during bootstrap."
                ),
            ),
        ]

        self._risks = risks
        return [risk.to_dict() for risk in risks]

    def opportunities(
        self,
        runtime: Any,
    ) -> list[dict[str, Any]]:
        opportunities = [
            PredictiveOpportunity(
                title="Compiled compatibility fabric",
                description=(
                    "Resolve verified legacy contracts during bootstrap and "
                    "retain direct immutable dispatch on the hot path."
                ),
                score=0.94,
                confidence=0.9,
                next_action=(
                    "Complete the remaining bounded domain adapters."
                ),
            ),
            PredictiveOpportunity(
                title="Architecture-aware capability validation",
                description=(
                    "Use SPA and bootstrap audits to detect stale runtime "
                    "bindings before release."
                ),
                score=0.9,
                confidence=0.88,
                next_action=(
                    "Add interface manifests to registration preflight."
                ),
            ),
        ]

        self._opportunities = opportunities
        return [
            opportunity.to_dict()
            for opportunity in opportunities
        ]

    def recommend(
        self,
        runtime: Any,
    ) -> list[dict[str, Any]]:
        recommendations = [
            PredictiveRecommendation(
                title="Repair bounded adapters first",
                recommendation=(
                    "Restore Workspace, Application, Semantic, Executive, "
                    "Planning, and UIL contracts through focused adapters."
                ),
                priority="critical",
                expected_gain=0.93,
                confidence=0.94,
            ),
            PredictiveRecommendation(
                title="Preserve compiled dispatch",
                recommendation=(
                    "Keep reflection and compatibility resolution confined "
                    "to bootstrap and retain O(1) runtime dispatch."
                ),
                priority="high",
                expected_gain=0.89,
                confidence=0.96,
            ),
        ]

        self._recommendations = recommendations
        return [
            recommendation.to_dict()
            for recommendation in recommendations
        ]

    def timeline(self, runtime: Any) -> list[dict[str, Any]]:
        events = []

        for forecast in self._forecasts:
            events.append(
                {
                    "type": "forecast",
                    "created_at": forecast.created_at,
                    "record": forecast.to_dict(),
                }
            )

        for scenario in self._scenarios:
            events.append(
                {
                    "type": "scenario",
                    "created_at": scenario.created_at,
                    "record": scenario.to_dict(),
                }
            )

        return sorted(
            events,
            key=lambda event: event["created_at"],
        )

    def statistics(self) -> dict[str, Any]:
        return {
            "version": self.VERSION,
            "forecasts": len(self._forecasts),
            "scenarios": len(self._scenarios),
            "risks": len(self._risks),
            "opportunities": len(self._opportunities),
            "recommendations": len(
                self._recommendations
            ),
            "engine_predictions": len(
                self.engine.list_predictions()
            ),
            "status": "operational",
        }

    def stats(self) -> dict[str, Any]:
        return self.statistics()
