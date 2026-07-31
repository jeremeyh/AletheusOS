"""Constitutional Policy Engine."""

from __future__ import annotations

from collections.abc import Iterable
from threading import RLock

from aletheus.platform_intelligence.constitutional_runtime_executive.models import (
    ExecutiveContext,
    ExecutiveDecision,
    ExecutiveRisk,
)
from aletheus.platform_intelligence.constitutional_runtime_executive.policies import (
    ExecutivePolicy,
)

from .exceptions import (
    PolicyAlreadyRegisteredError,
    PolicyEvaluationError,
    PolicyNotFoundError,
    PolicyRegistryFrozenError,
)
from .models import (
    ConstitutionalPolicyEngineState,
    PolicyEngineStatistics,
    PolicyEvaluation,
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


class ConstitutionalPolicyEngine:
    """
    Deterministic constitutional policy registry and evaluator.

    CPE owns policy registration, discovery, precedence, evaluation, and
    evidence aggregation. It never mutates runtime state or executes actions.
    """

    VERSION = "9.16.0"

    def __init__(
        self,
        policies: Iterable[ExecutivePolicy] = (),
        *,
        freeze: bool = False,
    ) -> None:
        self._policies: dict[
            str,
            ExecutivePolicy,
        ] = {}
        self._state = ConstitutionalPolicyEngineState.OPEN
        self._lock = RLock()

        self._evaluations = 0
        self._matched_evaluations = 0
        self._unmatched_evaluations = 0
        self._policy_matches = 0
        self._last_evaluation: PolicyEvaluation | None = None

        self.register_many(policies)

        if freeze:
            self.freeze()

    @property
    def state(
        self,
    ) -> ConstitutionalPolicyEngineState:
        return self._state

    @property
    def frozen(self) -> bool:
        return self._state is ConstitutionalPolicyEngineState.FROZEN

    def register(
        self,
        policy: ExecutivePolicy,
    ) -> ExecutivePolicy:
        with self._lock:
            if self.frozen:
                raise PolicyRegistryFrozenError("Policy registry is frozen.")

            policy_id = policy.policy_id.strip()

            if not policy_id:
                raise ValueError("Policy identifier cannot be empty.")

            if policy_id in self._policies:
                raise PolicyAlreadyRegisteredError(
                    f"Policy already registered: {policy_id}"
                )

            self._policies[policy_id] = policy

        return policy

    def register_many(
        self,
        policies: Iterable[ExecutivePolicy],
    ) -> tuple[ExecutivePolicy, ...]:
        return tuple(self.register(policy) for policy in policies)

    def get(
        self,
        policy_id: str,
    ) -> ExecutivePolicy:
        resolved = policy_id.strip()

        with self._lock:
            policy = self._policies.get(resolved)

        if policy is None:
            raise PolicyNotFoundError(f"Policy not found: {resolved}")

        return policy

    def all(
        self,
    ) -> tuple[ExecutivePolicy, ...]:
        with self._lock:
            return tuple(
                self._policies[policy_id] for policy_id in sorted(self._policies)
            )

    def freeze(self) -> None:
        with self._lock:
            self._state = ConstitutionalPolicyEngineState.FROZEN

    def evaluate(
        self,
        context: ExecutiveContext,
    ) -> PolicyEvaluation:
        try:
            results = tuple(policy.evaluate(context) for policy in self.all())
        except Exception as error:
            raise PolicyEvaluationError(
                "Constitutional policy evaluation failed."
            ) from error

        matched = tuple(result for result in results if result.matched)

        if matched:
            selected = max(
                matched,
                key=lambda result: (
                    _DECISION_PRECEDENCE[result.decision],
                    _RISK_PRECEDENCE[result.risk],
                    result.confidence,
                    result.policy_id,
                ),
            )

            evaluation = PolicyEvaluation.create(
                selected_decision=(selected.decision),
                selected_risk=selected.risk,
                selected_confidence=(selected.confidence),
                selected_reason=selected.reason,
                affected_services=(selected.affected_services),
                matched_policy_id=(selected.policy_id),
                results=results,
            )

            matched_count = len(matched)
        else:
            evaluation = PolicyEvaluation.create(
                selected_decision=(ExecutiveDecision.OBSERVE),
                selected_risk=(ExecutiveRisk.MODERATE),
                selected_confidence=0.5,
                selected_reason=(
                    "No constitutional policy fully matched; observation is required."
                ),
                affected_services=(context.recoverable_services),
                matched_policy_id=None,
                results=results,
            )

            matched_count = 0

        with self._lock:
            self._evaluations += 1
            self._policy_matches += matched_count

            if matched:
                self._matched_evaluations += 1
            else:
                self._unmatched_evaluations += 1

            self._last_evaluation = evaluation

        return evaluation

    def statistics(
        self,
    ) -> PolicyEngineStatistics:
        return PolicyEngineStatistics(
            registered_policies=len(self._policies),
            evaluations=self._evaluations,
            matched_evaluations=(self._matched_evaluations),
            unmatched_evaluations=(self._unmatched_evaluations),
            policy_matches=(self._policy_matches),
            frozen=self.frozen,
        )

    def snapshot(self) -> dict[str, object]:
        return {
            "version": self.VERSION,
            "state": self._state.value,
            "policies": [
                {
                    "policy_id": policy.policy_id,
                    "type": (policy.__class__.__name__),
                }
                for policy in self.all()
            ],
            "statistics": (self.statistics().to_dict()),
            "last_evaluation": (
                self._last_evaluation.to_dict() if self._last_evaluation else None
            ),
        }

    def export(self) -> dict[str, object]:
        return self.snapshot()
