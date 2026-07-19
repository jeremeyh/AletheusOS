"""Constitutional Runtime Governor."""

from __future__ import annotations

from collections import Counter, defaultdict
from datetime import UTC, datetime
from threading import RLock
from typing import Any

from aletheus.platform_intelligence.constitutional_runtime_executive import (
    ExecutiveDecision,
    ExecutiveRecoveryPlan,
)
from aletheus.platform_intelligence.constitutional_runtime_kernel import (
    ConstitutionalRuntimeKernel,
)

from .exceptions import (
    GovernorStateError,
    GovernorTargetNotFoundError,
)
from .models import (
    GovernorConstraints,
    GovernorDecision,
    GovernorMode,
    GovernorOutcome,
    GovernorRequest,
    GovernorStatistics,
)


class ConstitutionalRuntimeGovernor:
    """
    Operational enforcement authority for executive recovery plans.

    CRG evaluates whether an already-produced CRX plan may proceed under
    runtime constraints. It does not evaluate policy and never executes plans.
    """

    VERSION = "9.17.0"

    def __init__(
        self,
        *,
        kernel: ConstitutionalRuntimeKernel,
        constraints: GovernorConstraints | None = None,
    ) -> None:
        self._kernel = kernel
        self._constraints = (
            constraints or GovernorConstraints()
        )
        self._mode = GovernorMode.NORMAL
        self._lock = RLock()

        self._quarantined: set[str] = set()
        self._restart_counts: dict[str, int] = (
            defaultdict(int)
        )
        self._last_restart_at: dict[
            str,
            datetime,
        ] = {}
        self._outcomes: Counter[str] = Counter()
        self._evaluations = 0
        self._last_decision: (
            GovernorDecision | None
        ) = None

    @property
    def kernel(self) -> ConstitutionalRuntimeKernel:
        return self._kernel

    @property
    def mode(self) -> GovernorMode:
        return self._mode

    @property
    def constraints(self) -> GovernorConstraints:
        return self._constraints

    def set_mode(
        self,
        mode: GovernorMode,
    ) -> GovernorMode:
        with self._lock:
            if (
                self._mode is GovernorMode.EMERGENCY
                and mode is GovernorMode.NORMAL
            ):
                raise GovernorStateError(
                    "Emergency mode must transition "
                    "through maintenance."
                )

            self._mode = mode

        return self._mode

    def quarantine(
        self,
        address: str,
    ) -> None:
        resolved = self._normalize_target(address)
        self._require_target(resolved)

        with self._lock:
            self._quarantined.add(resolved)

    def release_quarantine(
        self,
        address: str,
    ) -> None:
        resolved = self._normalize_target(address)

        with self._lock:
            self._quarantined.discard(resolved)

    def is_quarantined(
        self,
        address: str,
    ) -> bool:
        return (
            self._normalize_target(address)
            in self._quarantined
        )

    def evaluate(
        self,
        plan: ExecutiveRecoveryPlan,
        *,
        requested_by: str = (
            "constitutional-runtime-executive"
        ),
    ) -> GovernorDecision:
        request = GovernorRequest.create(
            plan=plan,
            requested_by=requested_by,
        )

        for target in plan.target_services:
            self._require_target(target)

        if self._mode is GovernorMode.FROZEN:
            decision = GovernorDecision.create(
                request=request,
                outcome=GovernorOutcome.DENIED,
                approved=False,
                reason=(
                    "Runtime governance is frozen."
                ),
                requires_manual_approval=True,
            )
            return self._record(decision)

        if any(
            target in self._quarantined
            for target in plan.target_services
        ):
            decision = GovernorDecision.create(
                request=request,
                outcome=GovernorOutcome.DENIED,
                approved=False,
                reason=(
                    "One or more target services "
                    "are quarantined."
                ),
                requires_manual_approval=True,
            )
            return self._record(decision)

        if (
            len(plan.target_services)
            > self._constraints
            .maximum_concurrent_targets
        ):
            decision = GovernorDecision.create(
                request=request,
                outcome=GovernorOutcome.THROTTLED,
                approved=False,
                reason=(
                    "Plan exceeds the concurrent "
                    "target limit."
                ),
                requires_manual_approval=False,
            )
            return self._record(decision)

        if (
            plan.decision
            in self._constraints.manual_approval_for
            or plan.requires_manual_approval
        ):
            decision = GovernorDecision.create(
                request=request,
                outcome=GovernorOutcome.ESCALATED,
                approved=False,
                reason=(
                    "Plan requires manual approval."
                ),
                requires_manual_approval=True,
            )
            return self._record(decision)

        cooldown_decision = self._evaluate_cooldown(
            request
        )

        if cooldown_decision is not None:
            return self._record(
                cooldown_decision
            )

        budget_decision = self._evaluate_budget(
            request
        )

        if budget_decision is not None:
            return self._record(
                budget_decision
            )

        if self._mode is GovernorMode.MAINTENANCE:
            decision = GovernorDecision.create(
                request=request,
                outcome=GovernorOutcome.DEFERRED,
                approved=False,
                reason=(
                    "Plan deferred during maintenance."
                ),
                requires_manual_approval=False,
            )
            return self._record(decision)

        decision = GovernorDecision.create(
            request=request,
            outcome=GovernorOutcome.APPROVED,
            approved=True,
            reason=(
                "Plan satisfies active runtime "
                "governance constraints."
            ),
            requires_manual_approval=False,
        )

        return self._record(decision)

    def record_execution(
        self,
        plan: ExecutiveRecoveryPlan,
    ) -> None:
        """
        Record an approved plan after external execution.

        CRS or a future execution coordinator calls this after successful
        execution. CRG itself never executes the plan.
        """

        if plan.decision not in {
            ExecutiveDecision.RESTART_SERVICE,
            ExecutiveDecision.RESTART_DEPENDENCY_CHAIN,
        }:
            return

        now = datetime.now(UTC)

        with self._lock:
            for target in plan.target_services:
                self._restart_counts[target] += 1
                self._last_restart_at[target] = now

    def reset_budget(
        self,
        address: str,
    ) -> None:
        resolved = self._normalize_target(address)

        with self._lock:
            self._restart_counts.pop(
                resolved,
                None,
            )
            self._last_restart_at.pop(
                resolved,
                None,
            )

    def statistics(
        self,
    ) -> GovernorStatistics:
        return GovernorStatistics(
            evaluations=self._evaluations,
            approvals=self._outcomes[
                GovernorOutcome.APPROVED.value
            ],
            denials=self._outcomes[
                GovernorOutcome.DENIED.value
            ],
            deferrals=self._outcomes[
                GovernorOutcome.DEFERRED.value
            ],
            throttles=self._outcomes[
                GovernorOutcome.THROTTLED.value
            ],
            escalations=self._outcomes[
                GovernorOutcome.ESCALATED.value
            ],
            frozen=(
                self._mode is GovernorMode.FROZEN
            ),
            quarantined_services=len(
                self._quarantined
            ),
        )

    def snapshot(self) -> dict[str, Any]:
        return {
            "version": self.VERSION,
            "mode": self._mode.value,
            "constraints": {
                "maximum_restarts_per_target": (
                    self._constraints
                    .maximum_restarts_per_target
                ),
                "maximum_concurrent_targets": (
                    self._constraints
                    .maximum_concurrent_targets
                ),
                "restart_cooldown_seconds": (
                    self._constraints
                    .restart_cooldown
                    .total_seconds()
                ),
                "manual_approval_for": sorted(
                    decision.value
                    for decision
                    in self._constraints
                    .manual_approval_for
                ),
            },
            "quarantined_services": sorted(
                self._quarantined
            ),
            "restart_counts": dict(
                self._restart_counts
            ),
            "statistics": (
                self.statistics().to_dict()
            ),
            "last_decision": (
                self._last_decision.to_dict()
                if self._last_decision
                else None
            ),
        }

    def export(self) -> dict[str, Any]:
        return self.snapshot()

    def _evaluate_budget(
        self,
        request: GovernorRequest,
    ) -> GovernorDecision | None:
        if request.plan.decision not in {
            ExecutiveDecision.RESTART_SERVICE,
            ExecutiveDecision.RESTART_DEPENDENCY_CHAIN,
        }:
            return None

        exhausted = tuple(
            target
            for target in request.plan.target_services
            if self._restart_counts[target]
            >= self._constraints
            .maximum_restarts_per_target
        )

        if not exhausted:
            return None

        return GovernorDecision.create(
            request=request,
            outcome=GovernorOutcome.THROTTLED,
            approved=False,
            reason=(
                "Restart budget exhausted for: "
                + ", ".join(sorted(exhausted))
            ),
            requires_manual_approval=True,
        )

    def _evaluate_cooldown(
        self,
        request: GovernorRequest,
    ) -> GovernorDecision | None:
        if request.plan.decision not in {
            ExecutiveDecision.RESTART_SERVICE,
            ExecutiveDecision.RESTART_DEPENDENCY_CHAIN,
        }:
            return None

        now = datetime.now(UTC)
        blocked_until: list[datetime] = []

        for target in request.plan.target_services:
            last_restart = (
                self._last_restart_at.get(target)
            )

            if last_restart is None:
                continue

            retry_after = (
                last_restart
                + self._constraints
                .restart_cooldown
            )

            if now < retry_after:
                blocked_until.append(
                    retry_after
                )

        if not blocked_until:
            return None

        return GovernorDecision.create(
            request=request,
            outcome=GovernorOutcome.DEFERRED,
            approved=False,
            reason=(
                "Restart cooldown remains active."
            ),
            requires_manual_approval=False,
            retry_after=max(blocked_until),
        )

    def _record(
        self,
        decision: GovernorDecision,
    ) -> GovernorDecision:
        with self._lock:
            self._evaluations += 1
            self._outcomes[
                decision.outcome.value
            ] += 1
            self._last_decision = decision

        return decision

    def _require_target(
        self,
        address: str,
    ) -> None:
        try:
            self._kernel.service_registry.get(
                self._normalize_target(address)
            )
        except Exception as error:
            raise GovernorTargetNotFoundError(
                f"Governor target not found: "
                f"{address}"
            ) from error

    @staticmethod
    def _normalize_target(
        address: str,
    ) -> str:
        resolved = address.strip().lower()

        if not resolved:
            raise ValueError(
                "Governor target cannot be empty."
            )

        return resolved
