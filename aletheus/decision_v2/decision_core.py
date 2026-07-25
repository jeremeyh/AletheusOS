from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Any

from aletheus.time_utils import utc_now_iso


def now() -> str:
    return utc_now_iso()


@dataclass
class DecisionPolicy:
    name: str
    description: str
    weight: float = 1.0
    policy_type: str = "general"
    policy_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=now)

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__


@dataclass
class DecisionOption:
    title: str
    description: str = ""
    value_score: float = 0.5
    risk_score: float = 0.5
    confidence: float = 0.5
    cost_score: float = 0.5
    speed_score: float = 0.5
    option_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def weighted_score(self) -> float:
        score = (
            self.value_score * 0.3
            + (1 - self.risk_score) * 0.25
            + self.confidence * 0.25
            + self.cost_score * 0.1
            + self.speed_score * 0.1
        )
        return round(score, 2)

    def to_dict(self) -> dict[str, Any]:
        data = self.__dict__.copy()
        data["score"] = self.weighted_score()
        return data


@dataclass
class DecisionRecord:
    title: str
    objective: str
    options: list[DecisionOption]
    selected_option: dict[str, Any] | None = None
    confidence: float = 0.0
    status: str = "pending"
    reasoning_trace: dict[str, Any] = field(default_factory=dict)
    policy: str = "maximize_value"
    decision_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=now)
    executed_at: str | None = None
    rolled_back_at: str | None = None
    rollback_available: bool = True

    def execute(self) -> None:
        self.status = "executed"
        self.executed_at = now()

    def rollback(self) -> None:
        self.status = "rolled_back"
        self.rolled_back_at = now()

    def to_dict(self) -> dict[str, Any]:
        data = self.__dict__.copy()
        data["options"] = [option.to_dict() for option in self.options]
        return data


class AletheusAutonomousDecisionEngine:
    def __init__(self) -> None:
        self.version = "2.6.0"
        self.policies: dict[str, DecisionPolicy] = {}
        self.decisions: dict[str, DecisionRecord] = {}

    def bootstrap(self) -> dict[str, Any]:
        defaults = [
            ("maximize_value", "Prefer the highest expected value.", "value", 1.0),
            ("minimize_risk", "Prefer the lowest risk profile.", "risk", 1.0),
            ("maximize_confidence", "Prefer the option with highest confidence.", "confidence", 1.0),
            ("fastest_execution", "Prefer the fastest executable option.", "speed", 0.75),
            ("lowest_cost", "Prefer the lowest cost option.", "cost", 0.75),
            ("human_required", "Require founder approval before execution.", "governance", 1.0),
        ]
        for name, description, policy_type, weight in defaults:
            if name not in self.policies:
                self.add_policy(name, description, policy_type, weight)
        return self.stats()

    def add_policy(self, name: str, description: str, policy_type: str = "general", weight: float = 1.0) -> dict[str, Any]:
        policy = DecisionPolicy(name=name, description=description, policy_type=policy_type, weight=weight)
        self.policies[name] = policy
        return policy.to_dict()

    def evaluate(
        self,
        title: str,
        objective: str,
        options: list[dict[str, Any]],
        policy: str,
        runtime: Any,
    ) -> dict[str, Any]:
        if not self.policies:
            self.bootstrap()

        normalized = [
            DecisionOption(
                title=item.get("title", "Untitled Option"),
                description=item.get("description", ""),
                value_score=float(item.get("value_score", 0.5)),
                risk_score=float(item.get("risk_score", 0.5)),
                confidence=float(item.get("confidence", 0.5)),
                cost_score=float(item.get("cost_score", 0.5)),
                speed_score=float(item.get("speed_score", 0.5)),
            )
            for item in options
        ]

        if not normalized:
            normalized = [
                DecisionOption(
                    title="Gather more evidence",
                    description="Aletheus does not have enough options to execute.",
                    value_score=0.4,
                    risk_score=0.2,
                    confidence=0.7,
                    cost_score=0.9,
                    speed_score=0.8,
                )
            ]

        selected = max(normalized, key=lambda option: option.weighted_score())

        reasoning = runtime.commands.dispatch(
            "reason.evaluate",
            {
                "question": objective,
                "context": {
                    "decision_title": title,
                    "policy": policy,
                    "selected_option": selected.to_dict(),
                },
            },
        )

        reasoning_trace = reasoning.results.get("evaluation", {}) if not reasoning.errors else {
            "error": reasoning.errors,
            "confidence": selected.confidence,
        }

        confidence = round((selected.weighted_score() + float(reasoning_trace.get("confidence", selected.confidence))) / 2, 2)

        record = DecisionRecord(
            title=title,
            objective=objective,
            options=normalized,
            selected_option=selected.to_dict(),
            confidence=confidence,
            status="pending",
            reasoning_trace=reasoning_trace,
            policy=policy,
        )
        self.decisions[record.decision_id] = record
        return record.to_dict()

    def execute(self, decision_id: str) -> dict[str, Any]:
        decision = self.decisions.get(decision_id)
        if decision is None:
            return {"error": f"Decision not found: {decision_id}"}

        if decision.policy == "human_required":
            decision.status = "requires_founder_approval"
            return decision.to_dict()

        decision.execute()
        return decision.to_dict()

    def rollback(self, decision_id: str) -> dict[str, Any]:
        decision = self.decisions.get(decision_id)
        if decision is None:
            return {"error": f"Decision not found: {decision_id}"}

        if not decision.rollback_available:
            return {"error": "Rollback unavailable for this decision."}

        decision.rollback()
        return decision.to_dict()

    def explain(self, decision_id: str) -> dict[str, Any]:
        decision = self.decisions.get(decision_id)
        if decision is None:
            return {"error": f"Decision not found: {decision_id}"}

        selected = decision.selected_option or {}
        return {
            "decision_id": decision.decision_id,
            "title": decision.title,
            "selected_option": selected,
            "confidence": decision.confidence,
            "policy": decision.policy,
            "status": decision.status,
            "explanation": (
                f"Aletheus selected '{selected.get('title', 'unknown')}' because it had the strongest weighted score "
                f"under policy '{decision.policy}', with confidence {decision.confidence}."
            ),
            "reasoning_trace": decision.reasoning_trace,
        }

    def history(self) -> dict[str, Any]:
        return {
            "decisions": [decision.to_dict() for decision in self.decisions.values()]
        }

    def stats(self) -> dict[str, Any]:
        return {
            "version": self.version,
            "policies": len(self.policies),
            "decisions": len(self.decisions),
            "pending": len([d for d in self.decisions.values() if d.status == "pending"]),
            "executed": len([d for d in self.decisions.values() if d.status == "executed"]),
            "rolled_back": len([d for d in self.decisions.values() if d.status == "rolled_back"]),
            "average_confidence": round(
                sum(d.confidence for d in self.decisions.values()) / max(len(self.decisions), 1),
                2,
            ),
        }


decision_core = AletheusAutonomousDecisionEngine()
