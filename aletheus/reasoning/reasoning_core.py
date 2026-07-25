from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Any

from aletheus.time_utils import utc_now_iso


def now() -> str:
    return utc_now_iso()


@dataclass
class ReasoningRule:
    name: str
    description: str
    rule_type: str = "general"
    weight: float = 0.75
    rule_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=now)

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__


@dataclass
class DecisionTrace:
    question: str
    conclusion: str
    confidence: float
    supporting_facts: list[dict[str, Any]] = field(default_factory=list)
    rules_applied: list[dict[str, Any]] = field(default_factory=list)
    explanation: str = ""
    trace_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=now)

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__


class AletheusCognitiveReasoningEngine:
    def __init__(self) -> None:
        self.version = "2.5.0"
        self.rules: dict[str, ReasoningRule] = {}
        self.traces: list[DecisionTrace] = []

    def bootstrap_rules(self) -> dict[str, Any]:
        defaults = [
            ("Graph-supported conclusion", "Prefer conclusions supported by graph entities and relationships.", "graph", 0.90),
            ("Memory-supported conclusion", "Increase confidence when Memory Mesh evidence exists.", "memory", 0.85),
            ("Card Hawk strategic fit", "Card Hawk Foundation is the flagship native Aletheus application.", "cardhawk", 0.92),
            ("Founder approval gate", "Critical external actions require founder approval.", "governance", 0.95),
        ]
        for name, description, rule_type, weight in defaults:
            if not any(rule.name == name for rule in self.rules.values()):
                self.add_rule(name, description, rule_type, weight)
        return self.stats()

    def add_rule(self, name: str, description: str, rule_type: str = "general", weight: float = 0.75) -> dict[str, Any]:
        rule = ReasoningRule(name=name, description=description, rule_type=rule_type, weight=weight)
        self.rules[rule.rule_id] = rule
        return rule.to_dict()

    def evaluate(self, question: str, runtime: Any, context: dict[str, Any] | None = None) -> dict[str, Any]:
        context = context or {}

        graph_ctx = runtime.commands.dispatch("knowledge.search", {"query": question})
        memory_ctx = runtime.commands.dispatch("memory.mesh.search", {"query": question})
        infer_ctx = runtime.commands.dispatch("knowledge.infer", {})

        graph_results = graph_ctx.results.get("results", []) if not graph_ctx.errors else []
        memory_results = memory_ctx.results.get("results", []) if not memory_ctx.errors else []
        inference = infer_ctx.results.get("inference", {}) if not infer_ctx.errors else {}

        facts = []
        facts.extend([{"source": "knowledge_graph", "fact": item} for item in graph_results[:5]])
        facts.extend([{"source": "memory_mesh", "fact": item} for item in memory_results[:5]])

        if not self.rules:
            self.bootstrap_rules()

        rules = [rule.to_dict() for rule in self.rules.values()]

        confidence = 0.55
        confidence += min(len(graph_results) * 0.06, 0.18)
        confidence += min(len(memory_results) * 0.05, 0.15)
        confidence += min(len(inference.get("inferences", [])) * 0.04, 0.12)

        if "card hawk" in question.lower():
            confidence += 0.08

        if rules:
            confidence += 0.08

        confidence = round(min(confidence, 0.97), 2)

        conclusion = (
            "Aletheus found connected evidence and can produce a supported conclusion."
            if facts
            else "Aletheus has limited evidence and should gather more context before acting."
        )

        explanation = (
            f"Aletheus evaluated '{question}' using {len(facts)} supporting fact(s), "
            f"{len(rules)} rule(s), and graph inference context. Conclusion: {conclusion} "
            f"Confidence: {confidence}."
        )

        trace = DecisionTrace(
            question=question,
            conclusion=conclusion,
            confidence=confidence,
            supporting_facts=facts,
            rules_applied=rules,
            explanation=explanation,
        )
        self.traces.append(trace)
        return trace.to_dict()

    def explain(self, trace_id: str = "") -> dict[str, Any]:
        trace = None
        if trace_id:
            trace = next((item for item in self.traces if item.trace_id == trace_id), None)
        elif self.traces:
            trace = self.traces[-1]

        if trace is None:
            return {"error": "No reasoning trace found."}

        return {"explanation": trace.explanation, "trace": trace.to_dict()}

    def trace(self, trace_id: str = "") -> dict[str, Any]:
        if trace_id:
            item = next((trace for trace in self.traces if trace.trace_id == trace_id), None)
            return item.to_dict() if item else {"error": f"Trace not found: {trace_id}"}
        return {"traces": [item.to_dict() for item in self.traces]}

    def decision(self, question: str, runtime: Any, context: dict[str, Any] | None = None) -> dict[str, Any]:
        evaluation = self.evaluate(question=question, runtime=runtime, context=context)
        return {
            "decision": evaluation["conclusion"],
            "confidence": evaluation["confidence"],
            "trace_id": evaluation["trace_id"],
            "explanation": evaluation["explanation"],
        }

    def confidence(self) -> dict[str, Any]:
        if not self.traces:
            return {"confidence": 0.0, "decisions": 0}
        avg = sum(item.confidence for item in self.traces) / len(self.traces)
        return {"confidence": round(avg, 2), "decisions": len(self.traces)}

    def stats(self) -> dict[str, Any]:
        return {
            "version": self.version,
            "rules": len(self.rules),
            "traces": len(self.traces),
            "confidence": self.confidence()["confidence"],
        }


reasoning_core = AletheusCognitiveReasoningEngine()
