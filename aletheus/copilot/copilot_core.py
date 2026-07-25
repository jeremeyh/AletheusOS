from __future__ import annotations

from typing import Any

from aletheus.copilot.models import CopilotExchange, CopilotRecommendation


class AletheusFounderCopilot:
    def __init__(self) -> None:
        self.version = "1.5.0"
        self.exchanges: list[CopilotExchange] = []
        self.recommendations: list[CopilotRecommendation] = []

    def classify_intent(self, prompt: str) -> str:
        text = prompt.lower()
        if "plan" in text or "build" in text or "next" in text:
            return "planning"
        if "status" in text or "health" in text:
            return "status"
        if "recommend" in text or "should" in text:
            return "recommendation"
        if "why" in text or "explain" in text:
            return "explanation"
        return "general"

    def brief(self, runtime: Any) -> dict[str, Any]:
        summary = runtime.commands.dispatch("executive.summary", {}).results.get("summary", {})
        recommendations = runtime.commands.dispatch("executive.recommendations", {}).results.get("recommendations", [])
        risks = runtime.commands.dispatch("executive.risks", {}).results.get("risks", [])

        return {
            "title": "Founder Copilot Brief",
            "runtime_status": summary.get("overall_status", "unknown"),
            "highlights": summary.get("highlights", []),
            "recommendations": recommendations,
            "risks": risks,
        }

    def ask(self, prompt: str, runtime: Any) -> CopilotExchange:
        intent = self.classify_intent(prompt)
        actions: list[dict[str, Any]] = []

        if intent == "status":
            result = runtime.commands.dispatch("executive.summary", {})
            response = "Aletheus is online. Executive summary generated."
            actions.append({"command": "executive.summary", "result": result.results})

        elif intent == "planning":
            result = runtime.commands.dispatch(
                "planning.create",
                {"objective": prompt, "priority": "high"},
            )
            response = "I created an autonomous plan for this objective."
            actions.append({"command": "planning.create", "result": result.results})

        elif intent == "recommendation":
            result = runtime.commands.dispatch("executive.recommendations", {})
            response = "I generated executive recommendations based on current runtime state."
            actions.append({"command": "executive.recommendations", "result": result.results})

        elif intent == "explanation":
            result = runtime.commands.dispatch("executive.system_report", {})
            response = "I generated a system report to explain current state and reasoning."
            actions.append({"command": "executive.system_report", "result": result.results})

        else:
            result = runtime.commands.dispatch("workspace.overview", {})
            response = "I reviewed the Founder Workspace overview and current operating state."
            actions.append({"command": "workspace.overview", "result": result.results})

        exchange = CopilotExchange(
            prompt=prompt,
            response=response,
            intent=intent,
            actions=actions,
        )
        self.exchanges.append(exchange)
        return exchange

    def recommend(self, runtime: Any) -> list[dict[str, Any]]:
        health = runtime.commands.dispatch("runtime.health", {}).results.get("health", {})
        recs: list[CopilotRecommendation] = []

        if health.get("active_plans", 0) == 0:
            recs.append(
                CopilotRecommendation(
                    title="Create an active execution plan",
                    recommendation="Use the Autonomous Planning Engine to create a plan for the next Card Hawk Foundation integration milestone.",
                    priority="high",
                    confidence=0.92,
                )
            )

        if health.get("semantic_concepts", 0) < 5:
            recs.append(
                CopilotRecommendation(
                    title="Expand semantic intelligence",
                    recommendation="Bootstrap and enrich Card Hawk concepts so Aletheus can reason about the reference application more effectively.",
                    priority="medium",
                    confidence=0.87,
                )
            )

        if health.get("online_agents", 0) >= 6:
            recs.append(
                CopilotRecommendation(
                    title="Use multi-agent orchestration",
                    recommendation="Run a multi-agent orchestration against the current development objective.",
                    priority="medium",
                    confidence=0.84,
                )
            )

        self.recommendations.extend(recs)
        return [item.to_dict() for item in recs]

    def timeline(self, runtime: Any) -> dict[str, Any]:
        events = runtime.commands.dispatch("runtime.events", {}).results.get("events", [])
        memory = runtime.commands.dispatch("memory.recall", {"limit": 20}).results.get("memory", [])

        return {
            "events": events[-20:],
            "memory": memory[-20:],
            "exchanges": [item.to_dict() for item in self.exchanges[-20:]],
        }

    def history(self) -> list[dict[str, Any]]:
        return [item.to_dict() for item in self.exchanges]

    def stats(self) -> dict[str, Any]:
        return {
            "version": self.version,
            "exchanges": len(self.exchanges),
            "recommendations": len(self.recommendations),
        }


copilot_core = AletheusFounderCopilot()
