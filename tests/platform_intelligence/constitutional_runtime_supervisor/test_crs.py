from __future__ import annotations

import pytest

from aletheus.platform_intelligence import (
    ConstitutionalHealth,
    ConstitutionalRuntimeKernel,
    ConstitutionalRuntimeSupervisor,
    ConstitutionalRuntimeSupervisorState,
    ConstitutionalState,
    RestartPolicy,
    RuntimeSupervisionState,
    SupervisorLifecycleError,
    SupervisorServiceNotFoundError,
)


def build_supervisor(
    *,
    maximum_attempts: int = 3,
) -> ConstitutionalRuntimeSupervisor:
    kernel = ConstitutionalRuntimeKernel()

    return ConstitutionalRuntimeSupervisor(
        kernel=kernel,
        restart_policy=RestartPolicy(
            maximum_attempts=maximum_attempts
        ),
    )


def test_supervisor_starts_platform() -> None:
    supervisor = build_supervisor()

    report = supervisor.start_platform()

    assert supervisor.state is (
        ConstitutionalRuntimeSupervisorState.ACTIVE
    )
    assert report.state is (
        RuntimeSupervisionState.HEALTHY
    )
    assert report.healthy == report.service_count


def test_supervisor_stops_platform() -> None:
    supervisor = build_supervisor()

    supervisor.start_platform()
    report = supervisor.stop_platform()

    assert supervisor.state is (
        ConstitutionalRuntimeSupervisorState.STOPPED
    )
    assert report.state is (
        RuntimeSupervisionState.STOPPED
    )


def test_duplicate_start_is_rejected() -> None:
    supervisor = build_supervisor()

    supervisor.start_platform()

    with pytest.raises(
        SupervisorLifecycleError
    ):
        supervisor.start_platform()


def test_supervision_requires_active_state() -> None:
    supervisor = build_supervisor()

    with pytest.raises(
        SupervisorLifecycleError
    ):
        supervisor.supervise_once()


def test_heartbeat_is_recorded() -> None:
    supervisor = build_supervisor()

    supervisor.start_platform()

    stats = supervisor.statistics()

    assert stats.supervision_cycles == 1
    assert stats.heartbeats == 1


def test_runtime_health_detects_degradation() -> None:
    supervisor = build_supervisor()
    supervisor.start_platform()

    address = (
        "service.platform-intelligence."
        "runtime-explorer"
    )

    service = (
        supervisor.kernel.service_registry
        .report_health(
            address,
            ConstitutionalHealth.DEGRADED,
        )
    )

    supervisor.kernel.graph.update_node(
        service
    )

    report = supervisor.runtime_health()

    assert report.state is (
        RuntimeSupervisionState.DEGRADED
    )
    assert address in (
        report.recoverable_services
    )


def test_restart_service_uses_dependency_plan() -> None:
    supervisor = build_supervisor()
    supervisor.start_platform()

    address = (
        "service.platform-intelligence."
        "service-registry"
    )

    supervisor.restart_service(address)

    assert all(
        service.state
        is ConstitutionalState.RUNNING
        for service
        in supervisor.kernel
        .service_registry
        .all()
    )

    assert all(
        service.health
        is ConstitutionalHealth.HEALTHY
        for service
        in supervisor.kernel
        .service_registry
        .all()
    )


def test_auto_recovery_repairs_degraded_service() -> None:
    supervisor = build_supervisor()
    supervisor.start_platform()

    address = (
        "service.platform-intelligence."
        "runtime-explorer"
    )

    service = (
        supervisor.kernel.service_registry
        .report_health(
            address,
            ConstitutionalHealth.DEGRADED,
        )
    )

    supervisor.kernel.graph.update_node(
        service
    )

    report = supervisor.supervise_once(
        auto_recover=True
    )

    assert report.state is (
        RuntimeSupervisionState.HEALTHY
    )

    assert (
        supervisor.kernel.service_registry
        .get(address)
        .health
        is ConstitutionalHealth.HEALTHY
    )


def test_unknown_service_is_rejected() -> None:
    supervisor = build_supervisor()
    supervisor.start_platform()

    with pytest.raises(
        SupervisorServiceNotFoundError
    ):
        supervisor.restart_service(
            "service.missing"
        )


def test_export_contains_supervision_state() -> None:
    supervisor = build_supervisor()
    supervisor.start_platform()

    payload = supervisor.export()

    assert payload["state"] == "active"
    assert "runtime_health" in payload
    assert "statistics" in payload
    assert "restart_policy" in payload


def test_supervisor_does_not_own_dependency_logic() -> None:
    supervisor = build_supervisor()

    forbidden = {
        "build_boot_plan",
        "build_shutdown_plan",
        "build_restart_plan",
        "dependencies_of",
        "dependents_of",
        "register",
        "connect",
    }

    assert forbidden.isdisjoint(
        set(dir(supervisor))
    )
