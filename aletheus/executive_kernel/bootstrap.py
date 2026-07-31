from __future__ import annotations

from aletheus.executive_kernel.bus import ExecutiveBus
from aletheus.executive_kernel.capabilities import ExecutiveCapabilityRegistry
from aletheus.executive_kernel.composition import (
    ExecutiveComponentDescriptor,
    ExecutiveCompositionEngine,
)
from aletheus.executive_kernel.context import (
    ExecutiveContext,
    ExecutiveKnowledgeBase,
)
from aletheus.executive_kernel.decisions import ExecutiveDecisionEngine
from aletheus.executive_kernel.policies import ExecutivePolicyRegistry
from aletheus.executive_kernel.registry import ExecutiveKernelRegistry


class ExecutiveBootstrap:
    """
    Executive Bootstrap

    Sole responsibility:
        Build a valid Executive Context using the Executive Composition Engine.

    Kernels do not construct themselves. Bootstrap composes them.
    """

    def __init__(self) -> None:
        self.composition_engine = ExecutiveCompositionEngine()

    def configure_defaults(self) -> None:
        self.composition_engine.register(
            ExecutiveComponentDescriptor(
                component_id="executive_bus",
                name="Executive Bus",
                factory=lambda components: ExecutiveBus(),
            )
        )

        self.composition_engine.register(
            ExecutiveComponentDescriptor(
                component_id="kernel_registry",
                name="Executive Kernel Registry",
                factory=lambda components: ExecutiveKernelRegistry(),
            )
        )

        self.composition_engine.register(
            ExecutiveComponentDescriptor(
                component_id="capability_registry",
                name="Executive Capability Registry",
                factory=lambda components: ExecutiveCapabilityRegistry(),
            )
        )

        self.composition_engine.register(
            ExecutiveComponentDescriptor(
                component_id="policy_registry",
                name="Executive Policy Registry",
                factory=lambda components: ExecutivePolicyRegistry(),
            )
        )

        self.composition_engine.register(
            ExecutiveComponentDescriptor(
                component_id="knowledge_base",
                name="Executive Knowledge Base",
                dependencies=[
                    "kernel_registry",
                    "capability_registry",
                    "policy_registry",
                ],
                factory=lambda components: ExecutiveKnowledgeBase(
                    kernel_registry=components["kernel_registry"],
                    capability_registry=components["capability_registry"],
                    policy_registry=components["policy_registry"],
                ),
            )
        )

        self.composition_engine.register(
            ExecutiveComponentDescriptor(
                component_id="decision_engine",
                name="Executive Decision Engine",
                dependencies=[
                    "kernel_registry",
                    "capability_registry",
                    "policy_registry",
                ],
                factory=lambda components: ExecutiveDecisionEngine(
                    kernel_registry=components["kernel_registry"],
                    capability_registry=components["capability_registry"],
                    policy_registry=components["policy_registry"],
                ),
            )
        )

        self.composition_engine.register(
            ExecutiveComponentDescriptor(
                component_id="executive_context",
                name="Executive Context",
                dependencies=[
                    "executive_bus",
                    "knowledge_base",
                    "decision_engine",
                ],
                factory=lambda components: ExecutiveContext(
                    bus=components["executive_bus"],
                    knowledge_base=components["knowledge_base"],
                    decision_engine=components["decision_engine"],
                ),
            )
        )

    def build_context(self) -> ExecutiveContext:
        if not self.composition_engine.descriptors():
            self.configure_defaults()

        result = self.composition_engine.compose()

        if not result.success:
            raise RuntimeError(
                "Executive Bootstrap failed: " + "; ".join(result.errors)
            )

        return result.components["executive_context"]

    def summary(self) -> dict:
        return {
            "bootstrap": "Executive Bootstrap",
            "composition": self.composition_engine.dependency_graph(),
        }
