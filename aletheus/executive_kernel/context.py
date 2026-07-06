from __future__ import annotations

from dataclasses import dataclass

from aletheus.executive_kernel.bus import ExecutiveBus
from aletheus.executive_kernel.capabilities import ExecutiveCapabilityRegistry
from aletheus.executive_kernel.decisions import ExecutiveDecisionEngine
from aletheus.executive_kernel.policies import ExecutivePolicyRegistry
from aletheus.executive_kernel.registry import ExecutiveKernelRegistry


@dataclass(slots=True)
class ExecutiveKnowledgeBase:
    """
    Executive knowledge container.

    Registries describe executive knowledge. They do not execute.
    """

    kernel_registry: ExecutiveKernelRegistry
    capability_registry: ExecutiveCapabilityRegistry
    policy_registry: ExecutivePolicyRegistry

    def summary(self) -> dict:
        return {
            "kernel_registry": self.kernel_registry.summary(),
            "capability_registry": self.capability_registry.summary(),
            "policy_registry": self.policy_registry.summary(),
        }


@dataclass(slots=True)
class ExecutiveContext:
    """
    Composition context for the Executive Kernel.

    The Executive Kernel should remain small and rely on this context
    for its executive components.
    """

    bus: ExecutiveBus
    knowledge_base: ExecutiveKnowledgeBase
    decision_engine: ExecutiveDecisionEngine

    @classmethod
    def build(cls) -> "ExecutiveContext":
        bus = ExecutiveBus()
        kernel_registry = ExecutiveKernelRegistry()
        capability_registry = ExecutiveCapabilityRegistry()
        policy_registry = ExecutivePolicyRegistry()

        knowledge_base = ExecutiveKnowledgeBase(
            kernel_registry=kernel_registry,
            capability_registry=capability_registry,
            policy_registry=policy_registry,
        )

        decision_engine = ExecutiveDecisionEngine(
            kernel_registry=kernel_registry,
            capability_registry=capability_registry,
            policy_registry=policy_registry,
        )

        return cls(
            bus=bus,
            knowledge_base=knowledge_base,
            decision_engine=decision_engine,
        )
