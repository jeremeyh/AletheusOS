"""Constitutional Runtime Executive."""

from __future__ import annotations

from collections import Counter
from collections.abc import Iterable

from aletheus.platform_intelligence.constitutional_policy_engine import (
    ConstitutionalPolicyEngine,
)
from aletheus.platform_intelligence.constitutional_runtime_kernel import (
    ConstitutionalRuntimeKernel,
)
from aletheus.platform_intelligence.constitutional_runtime_supervisor import (
    ConstitutionalRuntimeSupervisor,
    RuntimeHealthReport,
)

from .exceptions import RecoveryPlanError
from .models import (
    ExecutiveContext,
    ExecutiveDecision,
    ExecutiveRecommendation,
    ExecutiveRecoveryPlan,
    ExecutiveRisk,
    ExecutiveStatistics,
)
from .policies import (
    ExecutivePolicy,
    default_executive_policies,
)

_DECISION_PRECEDENCE = {
    ExecutiveDecision.NO_ACTION: 0,
    ExecutiveDecision.OBSERVE: 10,
    ExecutiveDecision.RESTART_SERVICE: 20,
    ExecutiveDecision.RESTART_DEPENDENCY_CHAIN: 30,
    ExecutiveDecision.PAUSE_SERVICE: 40,
    ExecutiveDecision.STOP_RUNTIME: 50,
    ExecutiveDecision.REQUIRE_MANUAL_ACTION: 60,
    ExecutiveDecision.ESCALATE: 70,
}

_RISK_PRECEDENCE = {
    ExecutiveRisk.LOW: 0,
    ExecutiveRisk.MODERATE: 10,
    ExecutiveRisk.HIGH: 20,
    ExecutiveRisk.CRITICAL: 30,
}


class ConstitutionalRuntimeExecutive:
    """
    Policy-driven decision authority for runtime operations.

    CRX interprets runtime facts and produces recommendations and recovery
    plans. It never transitions services, restarts services, or executes plans.
    """

    VERSION = "9.15.0"

    def __init__(
        self,
        *,
        kernel: ConstitutionalRuntimeKernel,
        supervisor: (ConstitutionalRuntimeSupervisor),
        policies: Iterable[ExecutivePolicy] | None = None,
        policy_engine: (ConstitutionalPolicyEngine | None) = None,
    ) -> None:
        self._kernel = kernel
        self._supervisor = supervisor
        if policy_engine is not None and policies is not None:
            raise ValueError("Provide policies or policy_engine, not both.")

        self._policy_engine = policy_engine or ConstitutionalPolicyEngine(
            policies=(policies or default_executive_policies()),
            freeze=True,
        )

        self._evaluations = 0
        self._recommendations = 0
        self._decision_counts: Counter[str] = Counter()
        self._last_recommendation: ExecutiveRecommendation | None = None

    @property
    def kernel(self) -> ConstitutionalRuntimeKernel:
        return self._kernel

    @property
    def policy_engine(
        self,
    ) -> ConstitutionalPolicyEngine:
        return self._policy_engine

    @property
    def supervisor(
        self,
    ) -> ConstitutionalRuntimeSupervisor:
        return self._supervisor

    def context(
        self,
        report: RuntimeHealthReport | None = None,
    ) -> ExecutiveContext:
        health_report = report or self._supervisor.runtime_health()

        return ExecutiveContext.create(
            runtime_state=(health_report.state.value),
            kernel_state=(self._kernel.state.value),
            service_count=(health_report.service_count),
            healthy=health_report.healthy,
            warning=health_report.warning,
            degraded=health_report.degraded,
            critical=health_report.critical,
            offline=health_report.offline,
            unknown=health_report.unknown,
            recoverable_services=(health_report.recoverable_services),
            restart_attempts={
                record.address: (record.restart_attempts)
                for record in health_report.services
            },
        )

    def evaluate(
        self,
        report: RuntimeHealthReport | None = None,
    ) -> ExecutiveRecommendation:
        context = self.context(report)

        policy_evaluation = self._policy_engine.evaluate(context)

        decision = policy_evaluation.selected_decision

        recommendation = ExecutiveRecommendation.create(
            decision=decision,
            risk=(policy_evaluation.selected_risk),
            confidence=(policy_evaluation.selected_confidence),
            reason=(policy_evaluation.selected_reason),
            affected_services=(policy_evaluation.affected_services),
            policy_results=(policy_evaluation.results),
        )

        self._evaluations += 1
        self._recommendations += 1
        self._decision_counts[decision.value] += 1
        self._last_recommendation = recommendation

        return recommendation

    def plan(
        self,
        recommendation: (ExecutiveRecommendation),
    ) -> ExecutiveRecoveryPlan:
        decision = recommendation.decision
        targets = recommendation.affected_services

        if decision in {
            ExecutiveDecision.NO_ACTION,
            ExecutiveDecision.OBSERVE,
        }:
            return ExecutiveRecoveryPlan.create(
                decision=decision,
                target_services=targets,
                ordered_services=(),
                requires_manual_approval=False,
                rationale=recommendation.reason,
            )

        if decision is (ExecutiveDecision.RESTART_SERVICE):
            return ExecutiveRecoveryPlan.create(
                decision=decision,
                target_services=targets,
                ordered_services=targets,
                requires_manual_approval=False,
                rationale=recommendation.reason,
            )

        if decision is (ExecutiveDecision.RESTART_DEPENDENCY_CHAIN):
            ordered: list[str] = []

            for address in targets:
                restart_plan = self._kernel.restart_plan(address)

                for service in restart_plan.ordered_services:
                    if service not in ordered:
                        ordered.append(service)

            return ExecutiveRecoveryPlan.create(
                decision=decision,
                target_services=targets,
                ordered_services=tuple(ordered),
                requires_manual_approval=False,
                rationale=recommendation.reason,
            )

        if decision in {
            ExecutiveDecision.ESCALATE,
            ExecutiveDecision.REQUIRE_MANUAL_ACTION,
            ExecutiveDecision.STOP_RUNTIME,
            ExecutiveDecision.PAUSE_SERVICE,
        }:
            return ExecutiveRecoveryPlan.create(
                decision=decision,
                target_services=targets,
                ordered_services=(),
                requires_manual_approval=True,
                rationale=recommendation.reason,
            )

        raise RecoveryPlanError(f"Unsupported executive decision: {decision.value}")

    def decide_and_plan(
        self,
        report: RuntimeHealthReport | None = None,
    ) -> tuple[
        ExecutiveRecommendation,
        ExecutiveRecoveryPlan,
    ]:
        recommendation = self.evaluate(report)
        plan = self.plan(recommendation)

        return recommendation, plan

    def statistics(
        self,
    ) -> ExecutiveStatistics:
        return ExecutiveStatistics(
            evaluations=self._evaluations,
            recommendations=self._recommendations,
            no_action=self._decision_counts[ExecutiveDecision.NO_ACTION.value],
            observe=self._decision_counts[ExecutiveDecision.OBSERVE.value],
            restart_service=self._decision_counts[
                ExecutiveDecision.RESTART_SERVICE.value
            ],
            restart_dependency_chain=(
                self._decision_counts[ExecutiveDecision.RESTART_DEPENDENCY_CHAIN.value]
            ),
            escalations=self._decision_counts[ExecutiveDecision.ESCALATE.value],
            manual_actions=(
                self._decision_counts[ExecutiveDecision.REQUIRE_MANUAL_ACTION.value]
            ),
        )

    def export(self) -> dict[str, object]:
        return {
            "version": self.VERSION,
            "policy_count": (self._policy_engine.statistics().registered_policies),
            "policy_engine": (self._policy_engine.snapshot()),
            "statistics": (self.statistics().to_dict()),
            "last_recommendation": (
                self._last_recommendation.to_dict()
                if self._last_recommendation
                else None
            ),
        }
