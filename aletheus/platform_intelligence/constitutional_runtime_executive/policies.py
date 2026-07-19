"""Deterministic policies for the Constitutional Runtime Executive."""

from __future__ import annotations

from typing import Protocol

from .models import (
    ExecutiveContext,
    ExecutiveDecision,
    ExecutivePolicyResult,
    ExecutiveRisk,
)


class ExecutivePolicy(Protocol):
    """Contract for deterministic executive policies."""

    policy_id: str

    def evaluate(
        self,
        context: ExecutiveContext,
    ) -> ExecutivePolicyResult:
        """Evaluate one executive context."""


class CriticalRuntimePolicy:
    """Escalate when critical or offline services exist."""

    policy_id = "runtime.critical"

    def evaluate(
        self,
        context: ExecutiveContext,
    ) -> ExecutivePolicyResult:
        matched = bool(
            context.critical
            or context.offline
        )

        return ExecutivePolicyResult(
            policy_id=self.policy_id,
            matched=matched,
            decision=(
                ExecutiveDecision.ESCALATE
                if matched
                else ExecutiveDecision.NO_ACTION
            ),
            risk=(
                ExecutiveRisk.CRITICAL
                if matched
                else ExecutiveRisk.LOW
            ),
            confidence=1.0,
            reason=(
                "Critical or offline services require "
                "executive escalation."
                if matched
                else "No critical or offline services."
            ),
            affected_services=(
                context.recoverable_services
                if matched
                else ()
            ),
        )


class DegradedRuntimePolicy:
    """Recover dependency chains for degraded services."""

    policy_id = "runtime.degraded"

    def evaluate(
        self,
        context: ExecutiveContext,
    ) -> ExecutivePolicyResult:
        matched = bool(context.degraded)

        return ExecutivePolicyResult(
            policy_id=self.policy_id,
            matched=matched,
            decision=(
                ExecutiveDecision
                .RESTART_DEPENDENCY_CHAIN
                if matched
                else ExecutiveDecision.NO_ACTION
            ),
            risk=(
                ExecutiveRisk.HIGH
                if matched
                else ExecutiveRisk.LOW
            ),
            confidence=0.95,
            reason=(
                "Degraded services require "
                "dependency-aware recovery."
                if matched
                else "No degraded services."
            ),
            affected_services=(
                context.recoverable_services
                if matched
                else ()
            ),
        )


class WarningRuntimePolicy:
    """Observe warning-only runtime conditions."""

    policy_id = "runtime.warning"

    def evaluate(
        self,
        context: ExecutiveContext,
    ) -> ExecutivePolicyResult:
        matched = bool(
            context.warning
            and not context.degraded
            and not context.critical
            and not context.offline
        )

        return ExecutivePolicyResult(
            policy_id=self.policy_id,
            matched=matched,
            decision=(
                ExecutiveDecision.OBSERVE
                if matched
                else ExecutiveDecision.NO_ACTION
            ),
            risk=(
                ExecutiveRisk.MODERATE
                if matched
                else ExecutiveRisk.LOW
            ),
            confidence=0.9,
            reason=(
                "Warning-only conditions should be "
                "observed before intervention."
                if matched
                else "No warning-only condition."
            ),
            affected_services=(
                context.recoverable_services
                if matched
                else ()
            ),
        )


class HealthyRuntimePolicy:
    """Take no action when the runtime is healthy."""

    policy_id = "runtime.healthy"

    def evaluate(
        self,
        context: ExecutiveContext,
    ) -> ExecutivePolicyResult:
        matched = (
            context.runtime_state == "healthy"
            and context.healthy
            == context.service_count
        )

        return ExecutivePolicyResult(
            policy_id=self.policy_id,
            matched=matched,
            decision=ExecutiveDecision.NO_ACTION,
            risk=ExecutiveRisk.LOW,
            confidence=1.0,
            reason=(
                "Runtime is healthy; no action "
                "is required."
                if matched
                else "Runtime is not fully healthy."
            ),
            affected_services=(),
        )


def default_executive_policies(
) -> tuple[ExecutivePolicy, ...]:
    """Return canonical policies in precedence order."""

    return (
        CriticalRuntimePolicy(),
        DegradedRuntimePolicy(),
        WarningRuntimePolicy(),
        HealthyRuntimePolicy(),
    )
