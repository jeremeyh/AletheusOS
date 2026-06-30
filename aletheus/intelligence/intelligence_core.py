from __future__ import annotations

from typing import Any, Dict, List

from aletheus.intelligence.models import IntelligenceContext, IntelligenceDecision


class AletheusUniversalIntelligence:
    def __init__(self) -> None:
        self.version = "1.6.0"
        self.contexts: List[IntelligenceContext] = []
        self.decisions: List[IntelligenceDecision] = []

    def build_context(self, question: str, runtime: Any) -> IntelligenceContext:
        diagnostics = runtime.commands.dispatch("runtime.diagnostics", {}).results
        health = runtime.commands.dispatch("runtime.health", {}).results.get("health", {})

        context = IntelligenceContext(
            question=question,
            runtime=health,
            memory=diagnostics.get("memory", {}),
            knowledge=diagnostics.get("knowledge", {}),
            semantic=diagnostics.get("semantic", {}),
            planning=diagnostics.get("planning", {}),
            agents=diagnostics.get("agents", {}),
            executive=diagnostics.get("executive", {}),
            copilot=diagnostics.get("copilot", {}),
            applications=diagnostics.get("applications", {}),
        )
        self.contexts.append(context)
        return context

    def reason(self, question: str, runtime: Any) -> Dict[str, Any]:
        context = self.build_context(question, runtime)
        data = context.to_dict()

        reasoning = [
            f"Runtime status is {data['runtime'].get('status', 'unknown')}.",
            f"Aletheus version is {data['runtime'].get('version', 'unknown')}.",
            f"There are {data['runtime'].get('applications', 0)} registered applications.",
            f"There are {data['runtime'].get('memory_records', 0)} memory records available.",
            f"There are {data['runtime'].get('online_agents', 0)} online agents available for orchestration.",
        ]

        if data["runtime"].get("active_plans", 0) == 0:
            reasoning.append("No active autonomous plans are currently running.")

        if data["runtime"].get("semantic_concepts", 0) == 0:
            reasoning.append("Semantic concept density is low; semantic bootstrap should be prioritized.")

        return {
            "question": question,
            "context": data,
            "reasoning": reasoning,
            "confidence": self.confidence_score(data),
        }

    def synthesize(self, question: str, runtime: Any) -> Dict[str, Any]:
        reasoning_result = self.reason(question, runtime)
        runtime_data = reasoning_result["context"]["runtime"]

        facts = [
            f"Runtime online: {runtime_data.get('status') == 'online'}",
            f"Applications: {runtime_data.get('applications', 0)}",
            f"Agents online: {runtime_data.get('online_agents', 0)}",
            f"Memory records: {runtime_data.get('memory_records', 0)}",
            f"Semantic concepts: {runtime_data.get('semantic_concepts', 0)}",
        ]

        opportunities = []
        risks = []
        recommendations = []

        if runtime_data.get("applications", 0) >= 1:
            opportunities.append("Card Hawk Foundation is registered as a native Aletheus application.")

        if runtime_data.get("online_agents", 0) >= 6:
            opportunities.append("Multi-agent orchestration is available for complex work.")

        if runtime_data.get("semantic_concepts", 0) < 5:
            risks.append("Semantic layer remains under-seeded.")
            recommendations.append("Run Card Hawk semantic bootstrap and add core asset/player/service concepts.")

        if runtime_data.get("active_plans", 0) == 0:
            risks.append("No active autonomous plan is currently guiding execution.")
            recommendations.append("Create an autonomous plan for the next Card Hawk Foundation milestone.")

        recommendations.append("Continue integrating Card Hawk Foundation as the reference application.")

        return {
            "question": question,
            "facts": facts,
            "reasoning": reasoning_result["reasoning"],
            "opportunities": opportunities,
            "risks": risks,
            "recommendations": recommendations,
            "confidence": reasoning_result["confidence"],
        }

    def decide(self, question: str, runtime: Any) -> IntelligenceDecision:
        synthesis = self.synthesize(question, runtime)

        if synthesis["risks"]:
            decision = "Proceed, but address the identified gaps before expanding scope."
        else:
            decision = "Proceed with the next planned Aletheus/Card Hawk integration milestone."

        next_actions = synthesis["recommendations"][:3]

        item = IntelligenceDecision(
            question=question,
            decision=decision,
            confidence=synthesis["confidence"],
            reasoning=synthesis["reasoning"],
            risks=synthesis["risks"],
            next_actions=next_actions,
        )
        self.decisions.append(item)
        return item

    def brief(self, runtime: Any) -> Dict[str, Any]:
        question = "What is the current state of Aletheus?"
        synthesis = self.synthesize(question, runtime)
        decision = self.decide(question, runtime)

        return {
            "title": "Universal Intelligence Brief",
            "summary": "Aletheus has synthesized runtime, memory, knowledge, semantic, planning, agent, executive, copilot, and application context.",
            "synthesis": synthesis,
            "decision": decision.to_dict(),
        }

    def snapshot(self, runtime: Any) -> Dict[str, Any]:
        return {
            "version": self.version,
            "stats": self.stats(),
            "latest_context": self.contexts[-1].to_dict() if self.contexts else None,
            "latest_decision": self.decisions[-1].to_dict() if self.decisions else None,
            "runtime_health": runtime.commands.dispatch("runtime.health", {}).results.get("health", {}),
        }

    def confidence_score(self, context: Dict[str, Any]) -> float:
        score = 0.65
        runtime = context.get("runtime", {})

        if runtime.get("status") == "online":
            score += 0.1
        if runtime.get("applications", 0) >= 1:
            score += 0.05
        if runtime.get("online_agents", 0) >= 6:
            score += 0.08
        if runtime.get("memory_records", 0) >= 1:
            score += 0.04
        if runtime.get("semantic_concepts", 0) >= 5:
            score += 0.05
        if runtime.get("active_plans", 0) >= 1:
            score += 0.03

        return round(min(score, 0.98), 2)

    def timeline(self) -> Dict[str, Any]:
        return {
            "contexts": [item.to_dict() for item in self.contexts[-20:]],
            "decisions": [item.to_dict() for item in self.decisions[-20:]],
        }

    def stats(self) -> Dict[str, Any]:
        return {
            "version": self.version,
            "contexts": len(self.contexts),
            "decisions": len(self.decisions),
        }


intelligence_core = AletheusUniversalIntelligence()
