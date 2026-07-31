"""Constitutional Runtime Observatory."""

from __future__ import annotations

from datetime import UTC, datetime
from threading import RLock
from typing import Any
from uuid import UUID

from aletheus.platform_intelligence.constitutional_runtime_council import (
    ConstitutionalRuntimeCouncil,
)
from aletheus.platform_intelligence.constitutional_runtime_executive import (
    ConstitutionalRuntimeExecutive,
)
from aletheus.platform_intelligence.constitutional_runtime_governor import (
    ConstitutionalRuntimeGovernor,
)
from aletheus.platform_intelligence.constitutional_runtime_kernel import (
    ConstitutionalRuntimeKernel,
)
from aletheus.platform_intelligence.constitutional_runtime_supervisor import (
    ConstitutionalRuntimeSupervisor,
)

from .exceptions import (
    ObservatorySnapshotNotFoundError,
)
from .models import (
    ConstitutionalRuntimeHealthScore,
    ObservatoryDrift,
    ObservatoryDriftKind,
    ObservatoryExplanation,
    ObservatoryHealthBand,
    ObservatorySnapshot,
    ObservatoryStatistics,
    ObservatorySubsystemScore,
    ObservatoryTimelineEntry,
)


class ConstitutionalRuntimeObservatory:
    """
    Read-only observability authority for the constitutional runtime.

    CRO captures immutable snapshots, detects drift, scores constitutional
    health, explains observed state, and reconstructs runtime history. It owns
    no lifecycle, governance, policy, recovery, or execution authority.
    """

    VERSION = "9.19.0"

    def __init__(
        self,
        *,
        kernel: ConstitutionalRuntimeKernel,
        supervisor: ConstitutionalRuntimeSupervisor,
        executive: ConstitutionalRuntimeExecutive,
        governor: ConstitutionalRuntimeGovernor,
        council: ConstitutionalRuntimeCouncil,
    ) -> None:
        self._kernel = kernel
        self._supervisor = supervisor
        self._executive = executive
        self._governor = governor
        self._council = council

        self._snapshots: list[ObservatorySnapshot] = []
        self._timeline: list[ObservatoryTimelineEntry] = []
        self._baseline: ObservatorySnapshot | None = None
        self._explanations = 0
        self._lock = RLock()

    @property
    def baseline(
        self,
    ) -> ObservatorySnapshot | None:
        return self._baseline

    def capture(
        self,
        *,
        event_type: str = "runtime_observed",
        subject: str = "runtime",
        summary: str = ("Constitutional runtime snapshot captured."),
    ) -> ObservatorySnapshot:
        services = tuple(
            service.to_snapshot() for service in self._kernel.service_registry.all()
        )

        kernel = self._kernel.status().to_dict()
        supervisor = self._supervisor.export()
        executive = self._executive.export()
        policy_engine = self._executive.policy_engine.snapshot()
        governor = self._governor.snapshot()
        council = self._council.snapshot()
        dependency_manager = self._kernel.dependency_manager.export()

        health = self._score_health(
            services=services,
            supervisor=supervisor,
            dependency_manager=(dependency_manager),
            policy_engine=policy_engine,
            governor=governor,
            council=council,
        )

        drift = self._detect_drift(
            services=services,
            policy_engine=policy_engine,
            dependency_manager=(dependency_manager),
            governor=governor,
            council=council,
        )

        with self._lock:
            snapshot = ObservatorySnapshot.create(
                sequence=len(self._snapshots),
                kernel=kernel,
                supervisor=supervisor,
                executive=executive,
                policy_engine=policy_engine,
                governor=governor,
                council=council,
                dependency_manager=(dependency_manager),
                services=services,
                health=health,
                drift=drift,
            )

            self._snapshots.append(snapshot)

            if self._baseline is None:
                self._baseline = snapshot

            self._timeline.append(
                ObservatoryTimelineEntry(
                    sequence=len(self._timeline),
                    recorded_at=datetime.now(UTC),
                    event_type=event_type,
                    subject=subject,
                    summary=summary,
                    snapshot_id=(snapshot.snapshot_id),
                )
            )

        return snapshot

    def latest(self) -> ObservatorySnapshot:
        with self._lock:
            if not self._snapshots:
                raise (
                    ObservatorySnapshotNotFoundError("No observatory snapshots exist.")
                )

            return self._snapshots[-1]

    def get(
        self,
        snapshot_id: UUID,
    ) -> ObservatorySnapshot:
        with self._lock:
            for snapshot in self._snapshots:
                if snapshot.snapshot_id == snapshot_id:
                    return snapshot

        raise ObservatorySnapshotNotFoundError(f"Snapshot not found: {snapshot_id}")

    def snapshots(
        self,
    ) -> tuple[ObservatorySnapshot, ...]:
        with self._lock:
            return tuple(self._snapshots)

    def timeline(
        self,
    ) -> tuple[
        ObservatoryTimelineEntry,
        ...,
    ]:
        with self._lock:
            return tuple(self._timeline)

    def replay(
        self,
        *,
        start_sequence: int = 0,
        end_sequence: int | None = None,
    ) -> tuple[ObservatorySnapshot, ...]:
        with self._lock:
            return tuple(self._snapshots[start_sequence:end_sequence])

    def explain(
        self,
        subject: str,
    ) -> ObservatoryExplanation:
        snapshot = self.latest()
        resolved = subject.strip().lower()

        service = next(
            (
                item
                for item in snapshot.services
                if str(item.get("address", "")).lower() == resolved
            ),
            None,
        )

        if service is not None:
            state = str(service.get("state", "unknown"))
            health = str(service.get("health", "unknown"))
            attributes = service.get(
                "attributes",
                {},
            )

            explanation = f"{resolved} is in state {state} with health {health}."
            evidence = (
                f"state={state}",
                f"health={health}",
                (
                    "dependencies="
                    + str(
                        attributes.get(
                            "dependencies",
                            [],
                        )
                    )
                ),
            )
        elif resolved == "runtime":
            explanation = (
                "Runtime status is derived from the "
                "latest immutable constitutional "
                "snapshot."
            )
            evidence = (
                (
                    "kernel_state="
                    + str(
                        snapshot.kernel.get(
                            "state",
                            "unknown",
                        )
                    )
                ),
                ("constitutional_health=" + str(snapshot.health.overall_score)),
                ("drift_observations=" + str(len(snapshot.drift))),
            )
        else:
            explanation = f"No observed service matched {resolved}."
            evidence = (
                "subject_not_found=true",
                ("constitutional_health=" + str(snapshot.health.overall_score)),
            )

        with self._lock:
            self._explanations += 1

        return ObservatoryExplanation(
            subject=resolved,
            generated_at=datetime.now(UTC),
            explanation=explanation,
            evidence=evidence,
        )

    def statistics(
        self,
    ) -> ObservatoryStatistics:
        with self._lock:
            latest_score = (
                self._snapshots[-1].health.overall_score if self._snapshots else None
            )

            return ObservatoryStatistics(
                snapshots=len(self._snapshots),
                timeline_entries=len(self._timeline),
                drift_observations=sum(
                    len(snapshot.drift) for snapshot in self._snapshots
                ),
                explanations=(self._explanations),
                latest_health_score=(latest_score),
            )

    def snapshot(self) -> dict[str, Any]:
        return {
            "version": self.VERSION,
            "baseline_snapshot_id": (
                str(self._baseline.snapshot_id) if self._baseline else None
            ),
            "latest": (self._snapshots[-1].to_dict() if self._snapshots else None),
            "timeline": [entry.to_dict() for entry in self._timeline],
            "statistics": (self.statistics().to_dict()),
        }

    def export(self) -> dict[str, Any]:
        return {
            **self.snapshot(),
            "snapshots": [snapshot.to_dict() for snapshot in self._snapshots],
        }

    def _detect_drift(
        self,
        *,
        services: tuple[dict[str, Any], ...],
        policy_engine: dict[str, Any],
        dependency_manager: dict[str, Any],
        governor: dict[str, Any],
        council: dict[str, Any],
    ) -> tuple[ObservatoryDrift, ...]:
        baseline = self._baseline

        if baseline is None:
            return ()

        drift: list[ObservatoryDrift] = []

        baseline_services = {
            str(item.get("address")): item for item in baseline.services
        }
        observed_services = {str(item.get("address")): item for item in services}

        baseline_addresses = set(baseline_services)
        observed_addresses = set(observed_services)

        if baseline_addresses != observed_addresses:
            drift.append(
                ObservatoryDrift(
                    kind=(ObservatoryDriftKind.SERVICE_INVENTORY),
                    subject="runtime.services",
                    baseline=sorted(baseline_addresses),
                    observed=sorted(observed_addresses),
                    severity="high",
                    explanation=("Service inventory differs from the baseline."),
                )
            )

        for address in sorted(baseline_addresses & observed_addresses):
            before = baseline_services[address]
            after = observed_services[address]

            for field, kind, severity in (
                (
                    "state",
                    ObservatoryDriftKind.SERVICE_STATE,
                    "medium",
                ),
                (
                    "health",
                    ObservatoryDriftKind.SERVICE_HEALTH,
                    "high",
                ),
            ):
                if before.get(field) != after.get(field):
                    drift.append(
                        ObservatoryDrift(
                            kind=kind,
                            subject=address,
                            baseline=(before.get(field)),
                            observed=(after.get(field)),
                            severity=severity,
                            explanation=(f"{field} differs from the baseline."),
                        )
                    )

        before_policy_count = baseline.policy_engine.get("statistics", {}).get(
            "registered_policies"
        )
        after_policy_count = policy_engine.get("statistics", {}).get(
            "registered_policies"
        )

        if before_policy_count != after_policy_count:
            drift.append(
                ObservatoryDrift(
                    kind=(ObservatoryDriftKind.POLICY_REGISTRY),
                    subject="policy_engine",
                    baseline=before_policy_count,
                    observed=after_policy_count,
                    severity="high",
                    explanation=("Registered policy count differs from the baseline."),
                )
            )

        before_dependencies = baseline.dependency_manager.get("validation")
        after_dependencies = dependency_manager.get("validation")

        if before_dependencies != after_dependencies:
            drift.append(
                ObservatoryDrift(
                    kind=(ObservatoryDriftKind.DEPENDENCY_TOPOLOGY),
                    subject="dependency_manager",
                    baseline=before_dependencies,
                    observed=after_dependencies,
                    severity="high",
                    explanation=(
                        "Dependency validation state differs from the baseline."
                    ),
                )
            )

        before_governor = baseline.governor.get("mode")
        after_governor = governor.get("mode")

        if before_governor != after_governor:
            drift.append(
                ObservatoryDrift(
                    kind=(ObservatoryDriftKind.GOVERNANCE_STATE),
                    subject="runtime_governor",
                    baseline=before_governor,
                    observed=after_governor,
                    severity="medium",
                    explanation=("Governor mode differs from the baseline."),
                )
            )

        before_decisions = baseline.council.get("statistics", {}).get("decisions")
        after_decisions = council.get("statistics", {}).get("decisions")

        if before_decisions != after_decisions:
            drift.append(
                ObservatoryDrift(
                    kind=(ObservatoryDriftKind.GOVERNANCE_STATE),
                    subject="runtime_council",
                    baseline=before_decisions,
                    observed=after_decisions,
                    severity="low",
                    explanation=("Council decision count changed after baseline."),
                )
            )

        return tuple(drift)

    @classmethod
    def _score_health(
        cls,
        *,
        services: tuple[dict[str, Any], ...],
        supervisor: dict[str, Any],
        dependency_manager: dict[str, Any],
        policy_engine: dict[str, Any],
        governor: dict[str, Any],
        council: dict[str, Any],
    ) -> ConstitutionalRuntimeHealthScore:
        service_count = len(services)
        healthy_services = sum(
            str(item.get("health", "")).lower() == "healthy" for item in services
        )

        service_score = (
            100.0 if service_count == 0 else (healthy_services / service_count * 100.0)
        )

        dependency_valid = dependency_manager.get("validation", {}).get("valid", False)
        dependency_score = 100.0 if dependency_valid else 0.0

        policy_count = policy_engine.get("statistics", {}).get("registered_policies", 0)
        policy_score = 100.0 if policy_count > 0 else 50.0

        supervisor_state = str(supervisor.get("state", "")).lower()
        supervisor_score = 100.0 if supervisor_state == "active" else 60.0

        governor_mode = str(governor.get("mode", "")).lower()
        governor_score = {
            "normal": 100.0,
            "maintenance": 85.0,
            "frozen": 65.0,
            "emergency": 35.0,
        }.get(governor_mode, 50.0)

        active_members = council.get("statistics", {}).get("active_members", 0)
        council_score = 100.0 if active_members > 0 else 80.0

        raw_scores = (
            (
                "services",
                service_score,
                (f"{healthy_services}/{service_count} services are healthy."),
            ),
            (
                "dependencies",
                dependency_score,
                (
                    "Dependency topology is valid."
                    if dependency_valid
                    else ("Dependency topology is not validated.")
                ),
            ),
            (
                "policies",
                policy_score,
                (f"{policy_count} policies are registered."),
            ),
            (
                "supervisor",
                supervisor_score,
                (f"Supervisor state is {supervisor_state or 'unknown'}."),
            ),
            (
                "governor",
                governor_score,
                (f"Governor mode is {governor_mode or 'unknown'}."),
            ),
            (
                "council",
                council_score,
                (f"{active_members} active council members."),
            ),
        )

        subsystems = tuple(
            ObservatorySubsystemScore(
                subsystem=name,
                score=round(score, 2),
                band=cls._band(score),
                reason=reason,
            )
            for name, score, reason in raw_scores
        )

        overall = round(
            sum(item.score for item in subsystems) / len(subsystems),
            2,
        )

        return ConstitutionalRuntimeHealthScore(
            generated_at=datetime.now(UTC),
            overall_score=overall,
            band=cls._band(overall),
            subsystems=subsystems,
        )

    @staticmethod
    def _band(
        score: float,
    ) -> ObservatoryHealthBand:
        if score >= 95.0:
            return ObservatoryHealthBand.EXCELLENT

        if score >= 80.0:
            return ObservatoryHealthBand.HEALTHY

        if score >= 50.0:
            return ObservatoryHealthBand.DEGRADED

        return ObservatoryHealthBand.CRITICAL
