from __future__ import annotations

import pytest

from aletheus.platform_intelligence import (
    ConstitutionalHealth,
    ConstitutionalPolicyEngine,
    ConstitutionalRuntimeExecutive,
    ConstitutionalRuntimeKernel,
    ConstitutionalRuntimeSupervisor,
    ExecutiveDecision,
    ExecutiveRisk,
    PolicyAlreadyRegisteredError,
    PolicyRegistryFrozenError,
    default_executive_policies,
)


def build_context():
    kernel = ConstitutionalRuntimeKernel()

    supervisor = ConstitutionalRuntimeSupervisor(kernel=kernel)

    supervisor.start_platform()

    executive = ConstitutionalRuntimeExecutive(
        kernel=kernel,
        supervisor=supervisor,
    )

    return (
        kernel,
        supervisor,
        executive.context(),
    )


def test_policy_engine_registers_defaults() -> None:
    engine = ConstitutionalPolicyEngine(default_executive_policies())

    assert engine.statistics().registered_policies == 4


def test_duplicate_policy_is_rejected() -> None:
    policies = default_executive_policies()
    engine = ConstitutionalPolicyEngine()

    engine.register(policies[0])

    with pytest.raises(PolicyAlreadyRegisteredError):
        engine.register(policies[0])


def test_frozen_registry_rejects_mutation() -> None:
    policies = default_executive_policies()

    engine = ConstitutionalPolicyEngine(
        policies,
        freeze=True,
    )

    with pytest.raises(PolicyRegistryFrozenError):
        engine.register(policies[0])


def test_healthy_context_requires_no_action() -> None:
    _, _, context = build_context()

    engine = ConstitutionalPolicyEngine(
        default_executive_policies(),
        freeze=True,
    )

    evaluation = engine.evaluate(context)

    assert evaluation.selected_decision is (ExecutiveDecision.NO_ACTION)
    assert evaluation.selected_risk is (ExecutiveRisk.LOW)
    assert evaluation.matched_policy_id == ("runtime.healthy")


def test_degraded_context_selects_recovery() -> None:
    kernel, supervisor, _ = build_context()

    address = "service.platform-intelligence.service-registry"

    service = kernel.service_registry.report_health(
        address,
        ConstitutionalHealth.DEGRADED,
    )

    kernel.graph.update_node(service)

    executive = ConstitutionalRuntimeExecutive(
        kernel=kernel,
        supervisor=supervisor,
    )

    engine = executive.policy_engine
    evaluation = engine.evaluate(executive.context())

    assert evaluation.selected_decision is (ExecutiveDecision.RESTART_DEPENDENCY_CHAIN)
    assert evaluation.matched_policy_id == ("runtime.degraded")


def test_critical_policy_has_precedence() -> None:
    kernel, supervisor, _ = build_context()

    address = "service.platform-intelligence.runtime-explorer"

    service = kernel.service_registry.report_health(
        address,
        ConstitutionalHealth.CRITICAL,
    )

    kernel.graph.update_node(service)

    executive = ConstitutionalRuntimeExecutive(
        kernel=kernel,
        supervisor=supervisor,
    )

    evaluation = executive.policy_engine.evaluate(executive.context())

    assert evaluation.selected_decision is (ExecutiveDecision.ESCALATE)
    assert evaluation.selected_risk is (ExecutiveRisk.CRITICAL)


def test_statistics_track_evaluations() -> None:
    _, _, context = build_context()

    engine = ConstitutionalPolicyEngine(
        default_executive_policies(),
        freeze=True,
    )

    engine.evaluate(context)
    engine.evaluate(context)

    stats = engine.statistics()

    assert stats.evaluations == 2
    assert stats.matched_evaluations == 2
    assert stats.unmatched_evaluations == 0


def test_snapshot_is_auditable() -> None:
    _, _, context = build_context()

    engine = ConstitutionalPolicyEngine(
        default_executive_policies(),
        freeze=True,
    )

    engine.evaluate(context)

    snapshot = engine.snapshot()

    assert snapshot["version"] == "9.16.0"
    assert snapshot["state"] == "frozen"
    assert len(snapshot["policies"]) == 4
    assert snapshot["last_evaluation"] is not None


def test_policy_engine_is_read_only_at_runtime() -> None:
    engine = ConstitutionalPolicyEngine(
        default_executive_policies(),
        freeze=True,
    )

    forbidden = {
        "start",
        "stop",
        "restart",
        "execute",
        "transition",
        "report_health",
        "connect",
        "publish",
    }

    assert forbidden.isdisjoint(set(dir(engine)))
