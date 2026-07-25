from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .bootstrap import SPANBootstrap
from .finding import FindingSet
from .rule_engine import RuleEngine


@dataclass(slots=True)
class SPANIntegrationResult:
    pipeline_result: Any
    rule_findings: FindingSet


class SPANIntegration:
    """Coordinates bootstrap execution with rule evaluation."""

    def __init__(
        self,
        bootstrap: SPANBootstrap | None = None,
        rule_engine: RuleEngine | None = None,
    ) -> None:
        self.bootstrap = bootstrap or SPANBootstrap()
        self.rule_engine = rule_engine or RuleEngine()

    def register_rule(self, rule) -> None:
        self.rule_engine.register(rule)

    def run(self, project_root: str | Path, context: dict[str, Any] | None = None) -> SPANIntegrationResult:
        boot = self.bootstrap.run(project_root)
        findings = self.rule_engine.evaluate(context or {})
        return SPANIntegrationResult(
            pipeline_result=boot.pipeline_result,
            rule_findings=findings,
        )
