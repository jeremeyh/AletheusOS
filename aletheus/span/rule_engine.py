from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable

from .finding import Finding, FindingSet, Severity


@dataclass(slots=True)
class Rule:
    id: str
    title: str
    category: str
    severity: Severity
    predicate: Callable[[dict[str, Any]], bool]
    description: str = ""
    recommendation: str = ""
    confidence: float = 1.0
    tags: list[str] = field(default_factory=list)

    def evaluate(self, context: dict[str, Any]) -> Finding | None:
        if not self.predicate(context):
            return None
        return Finding(
            id=self.id,
            title=self.title,
            category=self.category,
            severity=self.severity,
            description=self.description or self.title,
            confidence=self.confidence,
            recommendation=self.recommendation,
            tags=self.tags,
            metadata={"rule_id": self.id},
        )


class RuleEngine:
    def __init__(self) -> None:
        self._rules: list[Rule] = []

    def register(self, rule: Rule) -> None:
        if any(r.id == rule.id for r in self._rules):
            raise ValueError(f"Duplicate rule id: {rule.id}")
        self._rules.append(rule)

    def evaluate(self, context: dict[str, Any]) -> FindingSet:
        findings = FindingSet()
        for rule in self._rules:
            finding = rule.evaluate(context)
            if finding is not None:
                findings.add(finding)
        return findings

    @property
    def rules(self) -> tuple[Rule, ...]:
        return tuple(self._rules)
