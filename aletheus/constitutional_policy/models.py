from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class ConstitutionalPolicy:
    policy_id: str
    name: str
    rule: str
    authority: str = "Principle X"
    description: str = ""
    enabled: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self):
        return {
            "policy_id": self.policy_id,
            "name": self.name,
            "rule": self.rule,
            "authority": self.authority,
            "description": self.description,
            "enabled": self.enabled,
            "metadata": self.metadata,
        }


@dataclass(slots=True)
class PolicyEvaluationResult:
    policy_id: str
    passed: bool
    reason: str
    evidence: dict[str, Any] = field(default_factory=dict)

    def to_dict(self):
        return {
            "policy_id": self.policy_id,
            "passed": self.passed,
            "reason": self.reason,
            "evidence": self.evidence,
        }
