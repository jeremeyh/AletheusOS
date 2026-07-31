from __future__ import annotations

from aletheus.platform_intelligence import (
    ConstitutionalHealth,
    ConstitutionalRuntimeExecutive,
    ConstitutionalRuntimeGovernor,
    ConstitutionalRuntimeKernel,
    ConstitutionalRuntimeSupervisor,
    ExecutiveDecision,
    GovernorOutcome,
)


def test_crx_plan_is_governed_before_execution() -> None:
    kernel = ConstitutionalRuntimeKernel()

    supervisor = ConstitutionalRuntimeSupervisor(kernel=kernel)
    supervisor.start_platform()

    executive = ConstitutionalRuntimeExecutive(
        kernel=kernel,
        supervisor=supervisor,
    )

    governor = ConstitutionalRuntimeGovernor(kernel=kernel)

    address = "service.platform-intelligence.runtime-explorer"

    service = kernel.service_registry.report_health(
        address,
        ConstitutionalHealth.DEGRADED,
    )
    kernel.graph.update_node(service)

    recommendation, plan = executive.decide_and_plan()

    assert recommendation.decision is (ExecutiveDecision.RESTART_DEPENDENCY_CHAIN)

    decision = governor.evaluate(plan)

    assert decision.outcome is (GovernorOutcome.APPROVED)
    assert decision.approved is True

    supervisor.restart_service(address)
    governor.record_execution(plan)

    assert kernel.service_registry.get(address).health is ConstitutionalHealth.HEALTHY
