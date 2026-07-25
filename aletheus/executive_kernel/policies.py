from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field
from enum import Enum


class PolicyScope(str, Enum):
    PLATFORM = "platform"
    KERNEL = "kernel"
    CAPABILITY = "capability"
    SERVICE = "service"
    APPLICATION = "application"


class PolicyDecision(str, Enum):
    ALLOW = "allow"
    DENY = "deny"
    CONDITIONAL = "conditional"


class PolicyTrustLevel(str, Enum):
    CONSTITUTIONAL = "constitutional"
    CERTIFIED = "certified"
    STANDARD = "standard"
    EXPERIMENTAL = "experimental"
    DEPRECATED = "deprecated"


@dataclass(slots=True)
class PolicyDescriptor:
    policy_id: str
    name: str
    scope: PolicyScope
    applies_to: str
    decision: PolicyDecision = PolicyDecision.CONDITIONAL
    trust_level: PolicyTrustLevel = PolicyTrustLevel.STANDARD
    version: str = "1.0"
    description: str = ""
    constraints: list[str] = field(default_factory=list)
    metadata: dict[str, str] = field(default_factory=dict)


class ExecutivePolicyRegistry:
    """
    Registry of executive governance policy declarations.

    Declares policy. It does not enforce policy directly.
    """

    def __init__(self) -> None:
        self._policies: dict[str, PolicyDescriptor] = {}

    def register(self, policy: PolicyDescriptor) -> None:
        self._policies[policy.policy_id] = policy

    def unregister(self, policy_id: str) -> None:
        self._policies.pop(policy_id, None)

    def get(self, policy_id: str) -> PolicyDescriptor | None:
        return self._policies.get(policy_id)

    def exists(self, policy_id: str) -> bool:
        return policy_id in self._policies

    def all(self) -> Iterable[PolicyDescriptor]:
        return self._policies.values()

    def by_scope(self, scope: PolicyScope) -> list[PolicyDescriptor]:
        return [
            policy
            for policy in self._policies.values()
            if policy.scope == scope
        ]

    def by_applies_to(self, target: str) -> list[PolicyDescriptor]:
        return [
            policy
            for policy in self._policies.values()
            if policy.applies_to == target
        ]

    def count(self) -> int:
        return len(self._policies)

    def summary(self) -> dict:
        return {
            "registered_policies": self.count(),
            "policies": [
                {
                    "id": policy.policy_id,
                    "name": policy.name,
                    "scope": policy.scope.value,
                    "applies_to": policy.applies_to,
                    "decision": policy.decision.value,
                    "trust_level": policy.trust_level.value,
                    "version": policy.version,
                    "constraints": policy.constraints,
                }
                for policy in self._policies.values()
            ],
        }
