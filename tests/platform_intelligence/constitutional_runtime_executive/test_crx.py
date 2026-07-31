from __future__ import annotations

from aletheus.platform_intelligence import (
    ConstitutionalHealth,
    ConstitutionalRuntimeExecutive,
    ConstitutionalRuntimeKernel,
    ConstitutionalRuntimeSupervisor,
    ExecutiveDecision,
    ExecutiveRisk,
)


def build_runtime():
    kernel = ConstitutionalRuntimeKernel()

    supervisor = ConstitutionalRuntimeSupervisor(kernel=kernel)

    supervisor.start_platform()

    executive = ConstitutionalRuntimeExecutive(
        kernel=kernel,
        supervisor=supervisor,
    )

    return kernel, supervisor, executive


def degrade(
    kernel: ConstitutionalRuntimeKernel,
    address: str,
    health: ConstitutionalHealth,
) -> None:
    service = kernel.service_registry.report_health(
        address,
        health,
    )

    kernel.graph.update_node(service)


def test_healthy_runtime_requires_no_action() -> None:
    _, _, executive = build_runtime()

    recommendation = executive.evaluate()

    assert recommendation.decision is (ExecutiveDecision.NO_ACTION)
    assert recommendation.risk is (ExecutiveRisk.LOW)


def test_warning_runtime_is_observed() -> None:
    kernel, _, executive = build_runtime()

    address = "service.platform-intelligence.runtime-explorer"

    degrade(
        kernel,
        address,
        ConstitutionalHealth.WARNING,
    )

    recommendation = executive.evaluate()

    assert recommendation.decision is (ExecutiveDecision.OBSERVE)
    assert address in (recommendation.affected_services)


def test_degraded_runtime_restarts_chain() -> None:
    kernel, _, executive = build_runtime()

    address = "service.platform-intelligence.service-registry"

    degrade(
        kernel,
        address,
        ConstitutionalHealth.DEGRADED,
    )

    recommendation = executive.evaluate()

    assert recommendation.decision is (ExecutiveDecision.RESTART_DEPENDENCY_CHAIN)
    assert recommendation.risk is (ExecutiveRisk.HIGH)


def test_critical_runtime_escalates() -> None:
    kernel, _, executive = build_runtime()

    address = "service.platform-intelligence.runtime-explorer"

    degrade(
        kernel,
        address,
        ConstitutionalHealth.CRITICAL,
    )

    recommendation = executive.evaluate()

    assert recommendation.decision is (ExecutiveDecision.ESCALATE)
    assert recommendation.risk is (ExecutiveRisk.CRITICAL)


def test_dependency_restart_plan_is_ordered() -> None:
    kernel, _, executive = build_runtime()

    address = "service.platform-intelligence.service-registry"

    degrade(
        kernel,
        address,
        ConstitutionalHealth.DEGRADED,
    )

    recommendation, plan = executive.decide_and_plan()

    assert recommendation.decision is (ExecutiveDecision.RESTART_DEPENDENCY_CHAIN)

    assert address in plan.ordered_services

    assert "service.platform-intelligence.digital-twin" in plan.ordered_services


def test_no_action_plan_is_empty() -> None:
    _, _, executive = build_runtime()

    recommendation, plan = executive.decide_and_plan()

    assert recommendation.decision is (ExecutiveDecision.NO_ACTION)
    assert plan.ordered_services == ()
    assert plan.requires_manual_approval is False


def test_escalation_requires_manual_approval() -> None:
    kernel, _, executive = build_runtime()

    address = "service.platform-intelligence.runtime-explorer"

    degrade(
        kernel,
        address,
        ConstitutionalHealth.CRITICAL,
    )

    _, plan = executive.decide_and_plan()

    assert plan.requires_manual_approval is True
    assert plan.ordered_services == ()


def test_statistics_track_decisions() -> None:
    _, _, executive = build_runtime()

    executive.evaluate()
    executive.evaluate()

    stats = executive.statistics()

    assert stats.evaluations == 2
    assert stats.recommendations == 2
    assert stats.no_action == 2


def test_export_contains_last_recommendation() -> None:
    _, _, executive = build_runtime()

    executive.evaluate()

    payload = executive.export()

    assert payload["version"] == "9.15.0"
    assert payload["last_recommendation"] is not None


def test_executive_does_not_execute_actions() -> None:
    _, _, executive = build_runtime()

    forbidden = {
        "start_platform",
        "stop_platform",
        "restart_service",
        "transition",
        "report_health",
        "execute",
        "publish",
        "connect",
    }

    assert forbidden.isdisjoint(set(dir(executive)))
