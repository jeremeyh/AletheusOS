from __future__ import annotations

from datetime import timedelta

import pytest

from aletheus.platform_intelligence import (
    ConstitutionalRuntimeExecutive,
    ConstitutionalRuntimeGovernor,
    ConstitutionalRuntimeKernel,
    ConstitutionalRuntimeSupervisor,
    ExecutiveDecision,
    ExecutiveRecoveryPlan,
    GovernorConstraints,
    GovernorMode,
    GovernorOutcome,
    GovernorStateError,
    GovernorTargetNotFoundError,
)


def build_runtime(
    *,
    constraints: GovernorConstraints | None = None,
):
    kernel = ConstitutionalRuntimeKernel()

    supervisor = (
        ConstitutionalRuntimeSupervisor(
            kernel=kernel
        )
    )
    supervisor.start_platform()

    executive = (
        ConstitutionalRuntimeExecutive(
            kernel=kernel,
            supervisor=supervisor,
        )
    )

    governor = (
        ConstitutionalRuntimeGovernor(
            kernel=kernel,
            constraints=constraints,
        )
    )

    return (
        kernel,
        supervisor,
        executive,
        governor,
    )


def plan_for(
    decision: ExecutiveDecision,
    *targets: str,
    manual: bool = False,
) -> ExecutiveRecoveryPlan:
    return ExecutiveRecoveryPlan.create(
        decision=decision,
        target_services=targets,
        ordered_services=targets,
        requires_manual_approval=manual,
        rationale="test plan",
    )


def test_safe_no_action_is_approved() -> None:
    _, _, _, governor = build_runtime()

    decision = governor.evaluate(
        plan_for(
            ExecutiveDecision.NO_ACTION
        )
    )

    assert decision.outcome is (
        GovernorOutcome.APPROVED
    )
    assert decision.approved is True


def test_restart_plan_is_approved() -> None:
    _, _, _, governor = build_runtime()

    address = (
        "service.platform-intelligence."
        "runtime-explorer"
    )

    decision = governor.evaluate(
        plan_for(
            ExecutiveDecision.RESTART_SERVICE,
            address,
        )
    )

    assert decision.outcome is (
        GovernorOutcome.APPROVED
    )


def test_frozen_runtime_denies_plan() -> None:
    _, _, _, governor = build_runtime()

    governor.set_mode(
        GovernorMode.FROZEN
    )

    address = (
        "service.platform-intelligence."
        "runtime-explorer"
    )

    decision = governor.evaluate(
        plan_for(
            ExecutiveDecision.RESTART_SERVICE,
            address,
        )
    )

    assert decision.outcome is (
        GovernorOutcome.DENIED
    )
    assert decision.approved is False


def test_quarantine_denies_target() -> None:
    _, _, _, governor = build_runtime()

    address = (
        "service.platform-intelligence."
        "runtime-explorer"
    )

    governor.quarantine(address)

    decision = governor.evaluate(
        plan_for(
            ExecutiveDecision.RESTART_SERVICE,
            address,
        )
    )

    assert decision.outcome is (
        GovernorOutcome.DENIED
    )


def test_manual_plan_is_escalated() -> None:
    _, _, _, governor = build_runtime()

    decision = governor.evaluate(
        plan_for(
            ExecutiveDecision.STOP_RUNTIME,
            manual=True,
        )
    )

    assert decision.outcome is (
        GovernorOutcome.ESCALATED
    )
    assert (
        decision.requires_manual_approval
        is True
    )


def test_target_limit_throttles_plan() -> None:
    constraints = GovernorConstraints(
        maximum_concurrent_targets=1
    )

    _, _, _, governor = build_runtime(
        constraints=constraints
    )

    decision = governor.evaluate(
        plan_for(
            ExecutiveDecision
            .RESTART_DEPENDENCY_CHAIN,
            (
                "service.platform-intelligence."
                "service-registry"
            ),
            (
                "service.platform-intelligence."
                "digital-twin"
            ),
        )
    )

    assert decision.outcome is (
        GovernorOutcome.THROTTLED
    )


def test_restart_budget_is_enforced() -> None:
    constraints = GovernorConstraints(
        maximum_restarts_per_target=1
    )

    _, _, _, governor = build_runtime(
        constraints=constraints
    )

    address = (
        "service.platform-intelligence."
        "runtime-explorer"
    )

    plan = plan_for(
        ExecutiveDecision.RESTART_SERVICE,
        address,
    )

    assert governor.evaluate(
        plan
    ).approved is True

    governor.record_execution(plan)

    decision = governor.evaluate(plan)

    assert decision.outcome is (
        GovernorOutcome.THROTTLED
    )


def test_restart_cooldown_defers_plan() -> None:
    constraints = GovernorConstraints(
        restart_cooldown=timedelta(
            minutes=5
        )
    )

    _, _, _, governor = build_runtime(
        constraints=constraints
    )

    address = (
        "service.platform-intelligence."
        "runtime-explorer"
    )

    plan = plan_for(
        ExecutiveDecision.RESTART_SERVICE,
        address,
    )

    assert governor.evaluate(
        plan
    ).approved is True

    governor.record_execution(plan)

    decision = governor.evaluate(plan)

    assert decision.outcome is (
        GovernorOutcome.DEFERRED
    )
    assert decision.retry_after is not None


def test_maintenance_defers_plan() -> None:
    _, _, _, governor = build_runtime()

    governor.set_mode(
        GovernorMode.MAINTENANCE
    )

    address = (
        "service.platform-intelligence."
        "runtime-explorer"
    )

    decision = governor.evaluate(
        plan_for(
            ExecutiveDecision.RESTART_SERVICE,
            address,
        )
    )

    assert decision.outcome is (
        GovernorOutcome.DEFERRED
    )


def test_unknown_target_is_rejected() -> None:
    _, _, _, governor = build_runtime()

    with pytest.raises(
        GovernorTargetNotFoundError
    ):
        governor.evaluate(
            plan_for(
                ExecutiveDecision.RESTART_SERVICE,
                "service.missing",
            )
        )


def test_emergency_cannot_jump_to_normal() -> None:
    _, _, _, governor = build_runtime()

    governor.set_mode(
        GovernorMode.EMERGENCY
    )

    with pytest.raises(
        GovernorStateError
    ):
        governor.set_mode(
            GovernorMode.NORMAL
        )


def test_snapshot_is_auditable() -> None:
    _, _, _, governor = build_runtime()

    governor.evaluate(
        plan_for(
            ExecutiveDecision.NO_ACTION
        )
    )

    snapshot = governor.snapshot()

    assert snapshot["version"] == "9.17.0"
    assert snapshot["mode"] == "normal"
    assert snapshot[
        "last_decision"
    ] is not None


def test_governor_never_executes() -> None:
    _, _, _, governor = build_runtime()

    forbidden = {
        "restart_service",
        "start_platform",
        "stop_platform",
        "transition",
        "report_health",
        "execute",
        "publish",
    }

    assert forbidden.isdisjoint(
        set(dir(governor))
    )
