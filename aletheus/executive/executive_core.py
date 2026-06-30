from __future__ import annotations

from typing import Any, Dict, List

from aletheus.executive.models import ExecutiveBrief, ExecutiveRecommendation, ExecutiveRisk


class AletheusExecutiveCore:
    def __init__(self) -> None:
        self.version = "1.2.0"
        self.recommendations: List[ExecutiveRecommendation] = []
        self.risks: List[ExecutiveRisk] = []
        self.briefs: List[ExecutiveBrief] = []

    def snapshot(self, runtime: Any) -> Dict[str, Any]:
        health = runtime.commands.dispatch("runtime.health").results.get("health", {})
        diagnostics = runtime.commands.dispatch("runtime.diagnostics").results

        return {
            "version": self.version,
            "runtime": health,
            "memory": diagnostics.get("memory", {}),
            "cognition": diagnostics.get("cognition", {}),
            "knowledge": diagnostics.get("knowledge", {}),
            "mission": diagnostics.get("mission", {}),
            "workspace": diagnostics.get("workspace", {}),
            "applications": diagnostics.get("applications", {}),
            "semantic": diagnostics.get("semantic", {}),
            "executive": self.stats(),
        }

    def summarize(self, runtime: Any) -> Dict[str, Any]:
        snap = self.snapshot(runtime)
        runtime_health = snap["runtime"]

        highlights = [
            f"Runtime status: {runtime_health.get('status', 'unknown')}.",
            f"Runtime version: {runtime_health.get('version', 'unknown')}.",
            f"Registered services: {runtime_health.get('services', 0)}.",
            f"Applications registered: {runtime_health.get('applications', 0)}.",
            f"Memory records: {runtime_health.get('memory_records', 0)}.",
            f"Semantic concepts: {runtime_health.get('semantic_concepts', 0)}.",
        ]

        return {
            "title": "Aletheus Executive Summary",
            "overall_status": "healthy" if runtime_health.get("status") == "online" else "attention_required",
            "highlights": highlights,
            "snapshot": snap,
        }

    def generate_recommendations(self, runtime: Any) -> List[Dict[str, Any]]:
        snap = self.snapshot(runtime)
        runtime_health = snap["runtime"]

        recommendations: List[ExecutiveRecommendation] = []

        if runtime_health.get("applications", 0) <= 1:
            recommendations.append(
                ExecutiveRecommendation(
                    title="Expand native application layer",
                    recommendation="Continue Card Hawk Foundation integration and prepare additional native applications for Aletheus.",
                    priority="high",
                    confidence=0.91,
                )
            )

        if runtime_health.get("semantic_concepts", 0) == 0:
            recommendations.append(
                ExecutiveRecommendation(
                    title="Bootstrap semantic intelligence",
                    recommendation="Run Card Hawk semantic bootstrap to seed Aletheus with application, service, and engine concepts.",
                    priority="high",
                    confidence=0.94,
                )
            )

        if runtime_health.get("active_missions", 0) == 0:
            recommendations.append(
                ExecutiveRecommendation(
                    title="Create active mission",
                    recommendation="Create a mission for Card Hawk Foundation integration so the Mission Engine can begin tracking execution.",
                    priority="medium",
                    confidence=0.86,
                )
            )

        if not recommendations:
            recommendations.append(
                ExecutiveRecommendation(
                    title="System operating normally",
                    recommendation="Continue expanding intelligence services and begin multi-agent orchestration preparation.",
                    priority="medium",
                    confidence=0.82,
                )
            )

        self.recommendations.extend(recommendations)
        return [item.to_dict() for item in recommendations]

    def analyze_risks(self, runtime: Any) -> List[Dict[str, Any]]:
        snap = self.snapshot(runtime)
        runtime_health = snap["runtime"]

        risks: List[ExecutiveRisk] = []

        if runtime_health.get("memory_records", 0) < 5:
            risks.append(
                ExecutiveRisk(
                    title="Low memory density",
                    description="Aletheus has very few memory records. Long-term reasoning will improve after more decisions, missions, and semantic assertions are captured.",
                    severity="medium",
                    confidence=0.88,
                )
            )

        if runtime_health.get("knowledge_entities", 0) == 0:
            risks.append(
                ExecutiveRisk(
                    title="Knowledge graph underpopulated",
                    description="The Knowledge Graph has no entities. Card Hawk Foundation should seed entities for applications, players, assets, services, and decisions.",
                    severity="medium",
                    confidence=0.9,
                )
            )

        if runtime_health.get("applications", 0) < 1:
            risks.append(
                ExecutiveRisk(
                    title="No native applications registered",
                    description="Aletheus needs at least one native application to validate the application runtime.",
                    severity="high",
                    confidence=0.95,
                )
            )

        self.risks.extend(risks)
        return [item.to_dict() for item in risks]

    def daily_brief(self, runtime: Any) -> Dict[str, Any]:
        summary = self.summarize(runtime)
        recommendations = self.generate_recommendations(runtime)
        risks = self.analyze_risks(runtime)

        brief = ExecutiveBrief(
            title="Founder Daily Brief",
            summary=f"Aletheus is {summary['overall_status']} with runtime version {summary['snapshot']['runtime'].get('version', 'unknown')}.",
            highlights=summary["highlights"],
            recommendations=recommendations,
            risks=risks,
        )
        self.briefs.append(brief)
        return brief.to_dict()

    def system_report(self, runtime: Any) -> Dict[str, Any]:
        return {
            "summary": self.summarize(runtime),
            "recommendations": self.generate_recommendations(runtime),
            "risks": self.analyze_risks(runtime),
            "stats": self.stats(),
        }

    def stats(self) -> Dict[str, Any]:
        return {
            "version": self.version,
            "recommendations": len(self.recommendations),
            "risks": len(self.risks),
            "briefs": len(self.briefs),
        }


executive_core = AletheusExecutiveCore()
