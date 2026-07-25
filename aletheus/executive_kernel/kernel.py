from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

from aletheus.executive_kernel.bootstrap import ExecutiveBootstrap
from aletheus.executive_kernel.bus import (
    ExecutiveBusEvent,
    ExecutiveBusEventType,
)
from aletheus.executive_kernel.capabilities import CapabilityDescriptor
from aletheus.executive_kernel.context import ExecutiveContext
from aletheus.executive_kernel.decisions import ExecutiveDecisionRequest
from aletheus.executive_kernel.policies import PolicyDescriptor
from aletheus.executive_kernel.registry import KernelDescriptor


def utc_now() -> str:
    return datetime.now(UTC).isoformat()


@dataclass
class ExecutiveKernelStatus:
    status: str
    message: str
    runtime_attached: bool
    generated_at: str = field(default_factory=utc_now)


class ExecutiveKernel:
    """
    AletheusOS Executive Kernel.

    Coordinates executive context, runtime attachment, and executive status.
    It does not replace runtime/core.py.
    """

    def __init__(
        self,
        context: ExecutiveContext | None = None,
    ) -> None:
        self.runtime: Any | None = None
        self.context = context or ExecutiveBootstrap().build_context()
        self.boot_events: list[dict[str, Any]] = []

    @property
    def bus(self):
        return self.context.bus

    @property
    def knowledge_base(self):
        return self.context.knowledge_base

    @property
    def kernel_registry(self):
        return self.context.knowledge_base.kernel_registry

    @property
    def capability_registry(self):
        return self.context.knowledge_base.capability_registry

    @property
    def policy_registry(self):
        return self.context.knowledge_base.policy_registry

    @property
    def decision_engine(self):
        return self.context.decision_engine

    def attach_runtime(self, runtime: Any) -> None:
        self.runtime = runtime
        event = {
            "event": "runtime_attached",
            "timestamp": utc_now(),
        }
        self.boot_events.append(event)
        self.bus.publish(
            ExecutiveBusEvent(
                event_type=ExecutiveBusEventType.RUNTIME_ATTACHED,
                source="executive_kernel",
                payload=event,
            )
        )

    def register_kernel(self, descriptor: KernelDescriptor) -> None:
        self.kernel_registry.register(descriptor)
        self.bus.publish(
            ExecutiveBusEvent(
                event_type=ExecutiveBusEventType.KERNEL_REGISTERED,
                source="executive_kernel",
                payload={
                    "kernel_id": descriptor.kernel_id,
                    "name": descriptor.name,
                    "version": descriptor.version,
                    "status": descriptor.status,
                },
            )
        )

    def register_capability(self, descriptor: CapabilityDescriptor) -> None:
        self.capability_registry.register(descriptor)
        self.bus.publish(
            ExecutiveBusEvent(
                event_type=ExecutiveBusEventType.CAPABILITY_REGISTERED,
                source="executive_kernel",
                payload={
                    "capability_id": descriptor.capability_id,
                    "name": descriptor.name,
                    "owner_kernel": descriptor.owner_kernel,
                    "provider": descriptor.provider,
                    "classification": descriptor.classification.value,
                    "trust_level": descriptor.trust_level.value,
                    "health": descriptor.health.value,
                },
            )
        )

    def register_policy(self, descriptor: PolicyDescriptor) -> None:
        self.policy_registry.register(descriptor)
        self.bus.publish(
            ExecutiveBusEvent(
                event_type=ExecutiveBusEventType.POLICY_REGISTERED,
                source="executive_kernel",
                payload={
                    "policy_id": descriptor.policy_id,
                    "name": descriptor.name,
                    "scope": descriptor.scope.value,
                    "applies_to": descriptor.applies_to,
                    "decision": descriptor.decision.value,
                    "trust_level": descriptor.trust_level.value,
                },
            )
        )

    def decide(self, request: ExecutiveDecisionRequest):
        self.bus.publish(
            ExecutiveBusEvent(
                event_type=ExecutiveBusEventType.DECISION_REQUESTED,
                source="executive_kernel",
                payload={
                    "capability_id": request.capability_id,
                    "requester": request.requester,
                    "intent_id": request.intent_id,
                },
            )
        )

        decision = self.decision_engine.decide(request)

        self.bus.publish(
            ExecutiveBusEvent(
                event_type=ExecutiveBusEventType.DECISION_COMPLETED,
                source="executive_kernel",
                payload={
                    "capability_id": decision.capability_id,
                    "status": decision.status.value,
                    "reason": decision.reason,
                    "requester": decision.requester,
                    "owner_kernel": decision.owner_kernel,
                    "provider": decision.provider,
                    "policy_ids": decision.policy_ids,
                    "constraints": decision.constraints,
                },
            )
        )

        return decision

    def status(self) -> ExecutiveKernelStatus:
        return ExecutiveKernelStatus(
            status="online" if self.runtime else "initializing",
            message=(
                "Executive Kernel online."
                if self.runtime
                else "Executive Kernel awaiting runtime attachment."
            ),
            runtime_attached=self.runtime is not None,
        )

    def boot_summary(self) -> dict:
        status = self.status()

        return {
            "kernel": "Executive Kernel",
            "status": status.status,
            "message": status.message,
            "runtime_attached": status.runtime_attached,
            "executive_context": {
                "knowledge_base": self.knowledge_base.summary(),
                "executive_bus": self.bus.summary(),
            },
            "boot_events": self.boot_events,
            "generated_at": status.generated_at,
        }
