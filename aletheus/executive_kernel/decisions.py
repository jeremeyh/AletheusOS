from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from aletheus.executive_kernel.capabilities import (
    CapabilityHealth,
    ExecutiveCapabilityRegistry,
)
from aletheus.executive_kernel.policies import (
    ExecutivePolicyRegistry,
    PolicyDecision,
)
from aletheus.executive_kernel.registry import ExecutiveKernelRegistry


class ExecutiveDecisionStatus(str, Enum):
    APPROVED = "approved"
    DENIED = "denied"
    CONDITIONAL = "conditional"
    UNKNOWN = "unknown"


@dataclass(slots=True)
class ExecutiveDecisionRequest:
    capability_id: str
    requester: str = "unknown"
    intent_id: str | None = None
    context: dict[str, str] = field(default_factory=dict)


@dataclass(slots=True)
class ExecutiveDecision:
    capability_id: str
    status: ExecutiveDecisionStatus
    reason: str
    requester: str = "unknown"
    owner_kernel: str | None = None
    provider: str | None = None
    policy_ids: list[str] = field(default_factory=list)
    constraints: list[str] = field(default_factory=list)


class ExecutiveDecisionEngine:
    """
    Evaluates executive capability requests against executive knowledge.

    It does not execute capabilities and does not mutate runtime.
    """

    def __init__(
        self,
        kernel_registry: ExecutiveKernelRegistry,
        capability_registry: ExecutiveCapabilityRegistry,
        policy_registry: ExecutivePolicyRegistry,
    ) -> None:
        self.kernel_registry = kernel_registry
        self.capability_registry = capability_registry
        self.policy_registry = policy_registry

    def decide(self, request: ExecutiveDecisionRequest) -> ExecutiveDecision:
        capability = self.capability_registry.get(request.capability_id)

        if capability is None:
            return ExecutiveDecision(
                capability_id=request.capability_id,
                requester=request.requester,
                status=ExecutiveDecisionStatus.UNKNOWN,
                reason="Capability is not registered.",
            )

        owner_kernel = self.kernel_registry.get(capability.owner_kernel)

        if owner_kernel is None:
            return ExecutiveDecision(
                capability_id=request.capability_id,
                requester=request.requester,
                status=ExecutiveDecisionStatus.DENIED,
                reason="Owner kernel is not registered.",
                owner_kernel=capability.owner_kernel,
                provider=capability.provider,
            )

        if capability.health == CapabilityHealth.OFFLINE:
            return ExecutiveDecision(
                capability_id=request.capability_id,
                requester=request.requester,
                status=ExecutiveDecisionStatus.DENIED,
                reason="Capability is offline.",
                owner_kernel=capability.owner_kernel,
                provider=capability.provider,
            )

        policies = self.policy_registry.by_applies_to(request.capability_id)

        if not policies:
            return ExecutiveDecision(
                capability_id=request.capability_id,
                requester=request.requester,
                status=ExecutiveDecisionStatus.CONDITIONAL,
                reason="No explicit policy found. Executive review required.",
                owner_kernel=capability.owner_kernel,
                provider=capability.provider,
            )

        policy_ids = [policy.policy_id for policy in policies]
        constraints: list[str] = []
        for policy in policies:
            constraints.extend(policy.constraints)

        if any(policy.decision == PolicyDecision.DENY for policy in policies):
            return ExecutiveDecision(
                capability_id=request.capability_id,
                requester=request.requester,
                status=ExecutiveDecisionStatus.DENIED,
                reason="At least one policy denies this capability.",
                owner_kernel=capability.owner_kernel,
                provider=capability.provider,
                policy_ids=policy_ids,
                constraints=constraints,
            )

        if any(policy.decision == PolicyDecision.CONDITIONAL for policy in policies):
            return ExecutiveDecision(
                capability_id=request.capability_id,
                requester=request.requester,
                status=ExecutiveDecisionStatus.CONDITIONAL,
                reason="Capability is conditionally permitted.",
                owner_kernel=capability.owner_kernel,
                provider=capability.provider,
                policy_ids=policy_ids,
                constraints=constraints,
            )

        return ExecutiveDecision(
            capability_id=request.capability_id,
            requester=request.requester,
            status=ExecutiveDecisionStatus.APPROVED,
            reason="Capability approved by executive policy.",
            owner_kernel=capability.owner_kernel,
            provider=capability.provider,
            policy_ids=policy_ids,
            constraints=constraints,
        )
