"""
SPAN Rule Registry

Canonical registry for declarative SPAN rules.
"""

from __future__ import annotations

from typing import Dict, Iterable

from .rule_engine import Rule, RuleEngine


class RuleRegistry:
    """Registry for SPAN Rule objects."""

    def __init__(self) -> None:
        self._rules: Dict[str, Rule] = {}
        self._enabled: set[str] = set()

    def register(self, rule: Rule) -> None:
        if rule.id in self._rules:
            raise ValueError(f"Rule already registered: {rule.id}")

        self._rules[rule.id] = rule
        self._enabled.add(rule.id)

    def unregister(self, rule_id: str) -> None:
        self._rules.pop(rule_id, None)
        self._enabled.discard(rule_id)

    def get(self, rule_id: str) -> Rule:
        return self._rules[rule_id]

    def list(self) -> tuple[Rule, ...]:
        return tuple(self._rules.values())

    def enabled(self) -> tuple[Rule, ...]:
        return tuple(
            self._rules[rid]
            for rid in sorted(self._enabled)
            if rid in self._rules
        )

    def enable(self, rule_id: str) -> None:
        if rule_id not in self._rules:
            raise KeyError(rule_id)

        self._enabled.add(rule_id)

    def disable(self, rule_id: str) -> None:
        self._enabled.discard(rule_id)

    def build_engine(self) -> RuleEngine:
        engine = RuleEngine()

        for rule in self.enabled():
            engine.register(rule)

        return engine

    def __len__(self) -> int:
        return len(self._rules)

    def __contains__(self, rule_id: str) -> bool:
        return rule_id in self._rules
