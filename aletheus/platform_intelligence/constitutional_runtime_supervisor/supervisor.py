"""Constitutional Runtime Supervisor."""

from __future__ import annotations

from collections import Counter, defaultdict
from datetime import UTC, datetime
from threading import RLock
from typing import Any

from aletheus.platform_intelligence.constitutional import (
    ConstitutionalHealth,
    ConstitutionalState,
)
from aletheus.platform_intelligence.constitutional_runtime_kernel import (
    ConstitutionalRuntimeKernel,
    ConstitutionalRuntimeKernelState,
)
from aletheus.platform_intelligence.events import (
    ConstitutionalEvent,
    ConstitutionalEventKind,
)

from .exceptions import (
    SupervisorLifecycleError,
    SupervisorRecoveryError,
    SupervisorServiceNotFoundError,
)
from .models import (
    ConstitutionalRuntimeSupervisorState,
    RestartPolicy,
    RuntimeHealthReport,
    RuntimeSupervisionState,
    ServiceSupervisionRecord,
    SupervisorHeartbeat,
    SupervisorStatistics,
)


class ConstitutionalRuntimeSupervisor:
    """
    Operational supervision authority for the constitutional runtime.

    CRS monitors health and coordinates dependency-aware recovery through
    CRK and CDM. It does not own services, dependency topology, or runtime
    composition.
    """

    VERSION = "9.14.0"

    def __init__(
        self,
        *,
        kernel: ConstitutionalRuntimeKernel,
        restart_policy: RestartPolicy | None = None,
    ) -> None:
        self._kernel = kernel
        self._restart_policy = restart_policy or RestartPolicy()
        self._state = ConstitutionalRuntimeSupervisorState.CREATED
        self._lock = RLock()

        self._supervision_cycles = 0
        self._heartbeat_sequence = 0
        self._recovery_attempts = 0
        self._successful_recoveries = 0
        self._failed_recoveries = 0
        self._service_restarts = 0

        self._restart_attempts: dict[str, int] = defaultdict(int)
        self._last_recovery_at: dict[
            str,
            datetime,
        ] = {}
        self._last_report: RuntimeHealthReport | None = None
        self._last_heartbeat: SupervisorHeartbeat | None = None

    @property
    def kernel(self) -> ConstitutionalRuntimeKernel:
        return self._kernel

    @property
    def state(
        self,
    ) -> ConstitutionalRuntimeSupervisorState:
        return self._state

    @property
    def active(self) -> bool:
        return self._state is ConstitutionalRuntimeSupervisorState.ACTIVE

    def start_platform(
        self,
    ) -> RuntimeHealthReport:
        with self._lock:
            if self._state is (ConstitutionalRuntimeSupervisorState.ACTIVE):
                raise SupervisorLifecycleError("CRS is already active.")

            if self._kernel.state in {
                ConstitutionalRuntimeKernelState.COMPOSED,
                ConstitutionalRuntimeKernelState.STOPPED,
            }:
                self._kernel.start()
            elif self._kernel.state is not (ConstitutionalRuntimeKernelState.RUNNING):
                raise SupervisorLifecycleError("Kernel is not in a startable state.")

            self._state = ConstitutionalRuntimeSupervisorState.ACTIVE

            self._publish_action(
                "supervisor_started",
                {
                    "version": self.VERSION,
                    "kernel_state": (self._kernel.state.value),
                },
            )

        return self.supervise_once()

    def stop_platform(
        self,
    ) -> RuntimeHealthReport:
        with self._lock:
            if not self.active:
                raise SupervisorLifecycleError("CRS can only stop while active.")

            if self._kernel.running:
                self._kernel.stop()

            self._state = ConstitutionalRuntimeSupervisorState.STOPPED

            self._publish_action(
                "supervisor_stopped",
                {
                    "kernel_state": (self._kernel.state.value),
                },
            )

        return self.runtime_health()

    def supervise_once(
        self,
        *,
        auto_recover: bool = False,
    ) -> RuntimeHealthReport:
        if not self.active:
            raise SupervisorLifecycleError("CRS must be active before supervision.")

        with self._lock:
            self._supervision_cycles += 1

        report = self.runtime_health()

        if auto_recover:
            for address in report.recoverable_services:
                if self._can_recover(address):
                    self.restart_service(address)

            report = self.runtime_health()

        self._last_report = report
        self.heartbeat(report)

        return report

    def runtime_health(
        self,
    ) -> RuntimeHealthReport:
        services = self._kernel.service_registry.all()

        health_counts = Counter(service.health.value for service in services)
        state_counts = Counter(service.state.value for service in services)

        records = tuple(
            ServiceSupervisionRecord(
                address=service.address,
                state=service.state.value,
                health=service.health.value,
                restart_attempts=(self._restart_attempts[service.address]),
                recoverable=(
                    service.health.value in self._restart_policy.recoverable_health
                ),
                last_recovery_at=(self._last_recovery_at.get(service.address)),
            )
            for service in services
        )

        recoverable = tuple(record.address for record in records if record.recoverable)

        state = self._derive_runtime_state(
            service_count=len(services),
            health_counts=health_counts,
            state_counts=state_counts,
        )

        return RuntimeHealthReport.create(
            state=state,
            service_count=len(services),
            healthy=health_counts["healthy"],
            warning=health_counts["warning"],
            degraded=health_counts["degraded"],
            critical=health_counts["critical"],
            offline=health_counts["offline"],
            unknown=health_counts["unknown"],
            running=state_counts["running"],
            stopped=state_counts["stopped"],
            recoverable_services=recoverable,
            services=records,
        )

    def restart_service(
        self,
        address: str,
    ) -> RuntimeHealthReport:
        resolved = address.strip().lower()

        try:
            self._kernel.service_registry.get(resolved)
        except Exception as error:
            raise SupervisorServiceNotFoundError(
                f"Service not found: {resolved}"
            ) from error

        if not self.active:
            raise SupervisorLifecycleError("CRS must be active before recovery.")

        if not self._can_recover(resolved):
            raise SupervisorRecoveryError(
                f"Restart policy does not permit another attempt for {resolved}."
            )

        with self._lock:
            self._recovery_attempts += 1
            self._restart_attempts[resolved] += 1

        plan = self._kernel.restart_plan(resolved)

        self._publish_action(
            "recovery_started",
            {
                "service": resolved,
                "affected_services": list(plan.ordered_services),
                "attempt": (self._restart_attempts[resolved]),
            },
        )

        try:
            for level in reversed(plan.levels):
                for service_address in level.services:
                    self._stop_service(service_address)

            for level in plan.levels:
                for service_address in level.services:
                    self._start_service(service_address)
                    self._service_restarts += 1

            now = datetime.now(UTC)

            with self._lock:
                self._successful_recoveries += 1
                self._last_recovery_at[resolved] = now

            self._publish_action(
                "recovery_completed",
                {
                    "service": resolved,
                    "affected_services": list(plan.ordered_services),
                },
            )

        except Exception as error:
            with self._lock:
                self._failed_recoveries += 1

            self._publish_action(
                "recovery_failed",
                {
                    "service": resolved,
                    "error": str(error),
                },
            )

            raise SupervisorRecoveryError(f"Recovery failed for {resolved}.") from error

        return self.runtime_health()

    def heartbeat(
        self,
        report: RuntimeHealthReport | None = None,
    ) -> SupervisorHeartbeat:
        current_report = report or self.runtime_health()

        with self._lock:
            self._heartbeat_sequence += 1

            heartbeat = SupervisorHeartbeat(
                sequence=self._heartbeat_sequence,
                generated_at=datetime.now(UTC),
                supervisor_state=self._state,
                runtime_state=current_report.state,
                kernel_state=(self._kernel.state.value),
                service_count=(current_report.service_count),
                degraded_count=(
                    current_report.warning
                    + current_report.degraded
                    + current_report.critical
                    + current_report.offline
                ),
                recovery_count=(self._successful_recoveries),
                restart_count=(self._service_restarts),
            )

            self._last_heartbeat = heartbeat

        self._publish_action(
            "supervisor_heartbeat",
            heartbeat.to_dict(),
        )

        return heartbeat

    def statistics(
        self,
    ) -> SupervisorStatistics:
        return SupervisorStatistics(
            supervision_cycles=(self._supervision_cycles),
            heartbeats=self._heartbeat_sequence,
            recovery_attempts=(self._recovery_attempts),
            successful_recoveries=(self._successful_recoveries),
            failed_recoveries=(self._failed_recoveries),
            service_restarts=(self._service_restarts),
            monitored_services=(self._kernel.service_registry.statistics().registered),
        )

    def export(self) -> dict[str, Any]:
        report = self._last_report or self.runtime_health()

        return {
            "version": self.VERSION,
            "state": self._state.value,
            "runtime_health": report.to_dict(),
            "heartbeat": (
                self._last_heartbeat.to_dict() if self._last_heartbeat else None
            ),
            "statistics": (self.statistics().to_dict()),
            "restart_policy": {
                "maximum_attempts": (self._restart_policy.maximum_attempts),
                "cooldown_seconds": (self._restart_policy.cooldown.total_seconds()),
                "recoverable_health": sorted(self._restart_policy.recoverable_health),
            },
        }

    def _start_service(
        self,
        address: str,
    ) -> None:
        service = self._kernel.service_registry.get(address)

        if service.state is (ConstitutionalState.RUNNING):
            return

        if service.state is (ConstitutionalState.REGISTERED):
            states = (
                ConstitutionalState.INITIALIZING,
                ConstitutionalState.STARTING,
                ConstitutionalState.RUNNING,
            )
        elif service.state is (ConstitutionalState.STOPPED):
            states = (
                ConstitutionalState.STARTING,
                ConstitutionalState.RUNNING,
            )
        elif service.state is (ConstitutionalState.DEGRADED):
            states = (
                ConstitutionalState.RECOVERING,
                ConstitutionalState.RUNNING,
            )
        elif service.state is (ConstitutionalState.PAUSED):
            states = (ConstitutionalState.RUNNING,)
        else:
            states = ()

        transitioned = service

        for state in states:
            transitioned = self._kernel.service_registry.transition(
                transitioned.address,
                state,
            )

        transitioned = self._kernel.service_registry.report_health(
            transitioned.address,
            ConstitutionalHealth.HEALTHY,
        )

        self._kernel.graph.update_node(transitioned)

    def _stop_service(
        self,
        address: str,
    ) -> None:
        service = self._kernel.service_registry.get(address)

        if service.state is (ConstitutionalState.STOPPED):
            return

        if service.state in {
            ConstitutionalState.RUNNING,
            ConstitutionalState.PAUSED,
            ConstitutionalState.DEGRADED,
            ConstitutionalState.RECOVERING,
            ConstitutionalState.INITIALIZING,
            ConstitutionalState.STARTING,
        }:
            service = self._kernel.service_registry.transition(
                service.address,
                ConstitutionalState.STOPPING,
            )

            service = self._kernel.service_registry.transition(
                service.address,
                ConstitutionalState.STOPPED,
            )

            self._kernel.graph.update_node(service)

    def _can_recover(
        self,
        address: str,
    ) -> bool:
        attempts = self._restart_attempts[address]

        if attempts >= (self._restart_policy.maximum_attempts):
            return False

        last_recovery = self._last_recovery_at.get(address)

        if last_recovery is None:
            return True

        return datetime.now(UTC) - last_recovery >= self._restart_policy.cooldown

    @staticmethod
    def _derive_runtime_state(
        *,
        service_count: int,
        health_counts: Counter[str],
        state_counts: Counter[str],
    ) -> RuntimeSupervisionState:
        if service_count == 0:
            return RuntimeSupervisionState.UNKNOWN

        if state_counts["stopped"] == service_count:
            return RuntimeSupervisionState.STOPPED

        if health_counts["critical"] or health_counts["offline"]:
            return RuntimeSupervisionState.UNAVAILABLE

        if (
            health_counts["warning"]
            or health_counts["degraded"]
            or health_counts["unknown"]
        ):
            return RuntimeSupervisionState.DEGRADED

        if (
            health_counts["healthy"] == service_count
            and state_counts["running"] == service_count
        ):
            return RuntimeSupervisionState.HEALTHY

        return RuntimeSupervisionState.UNKNOWN

    def _publish_action(
        self,
        action: str,
        payload: dict[str, Any],
    ) -> None:
        self._kernel.event_bus.publish(
            ConstitutionalEvent.create(
                kind=(ConstitutionalEventKind.STATE_CHANGED),
                source=("service.platform-intelligence.runtime-supervisor"),
                subject=("service.platform-intelligence.runtime-supervisor"),
                payload={
                    "action": action,
                    **payload,
                },
            )
        )
