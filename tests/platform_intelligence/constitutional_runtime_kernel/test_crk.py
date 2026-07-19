from __future__ import annotations

import pytest

from aletheus.platform_intelligence import (
    ConstitutionalRuntimeKernel,
    ConstitutionalRuntimeKernelState,
    KernelLifecycleError,
)


def test_kernel_auto_composes() -> None:
    kernel = ConstitutionalRuntimeKernel()

    assert kernel.state is (
        ConstitutionalRuntimeKernelState.COMPOSED
    )
    assert kernel.composed is True
    assert kernel.running is False


def test_kernel_exposes_all_components() -> None:
    kernel = ConstitutionalRuntimeKernel()

    assert kernel.event_bus is not None
    assert kernel.service_registry is not None
    assert kernel.graph is not None
    assert kernel.digital_twin is not None
    assert kernel.runtime_explorer is not None
    assert kernel.intelligence_engine is not None
    assert kernel.mission_engine is not None
    assert kernel.mission_scheduler is not None
    assert kernel.orchestrator is not None


def test_kernel_registers_canonical_services() -> None:
    kernel = ConstitutionalRuntimeKernel()

    stats = kernel.service_registry.statistics()

    assert stats.registered == 10

    addresses = {
        service.address
        for service in kernel.service_registry.all()
    }

    assert (
        "service.platform-intelligence.crk"
        in addresses
    )
    assert (
        "service.platform-intelligence.digital-twin"
        in addresses
    )
    assert (
        "service.platform-intelligence.mission-engine"
        in addresses
    )


def test_kernel_builds_constitutional_graph() -> None:
    kernel = ConstitutionalRuntimeKernel()

    stats = kernel.graph.statistics()

    assert stats.nodes == 10
    assert stats.relationships > 0
    assert stats.cycles == 0


def test_kernel_start_transitions_services() -> None:
    kernel = ConstitutionalRuntimeKernel()

    status = kernel.start()

    assert status.state is (
        ConstitutionalRuntimeKernelState.RUNNING
    )
    assert status.running is True
    assert status.registered_services == 10

    assert all(
        service.state.value == "running"
        for service in kernel.service_registry.all()
    )

    assert all(
        service.health.value == "healthy"
        for service in kernel.service_registry.all()
    )


def test_kernel_stop_transitions_services() -> None:
    kernel = ConstitutionalRuntimeKernel()

    kernel.start()
    status = kernel.stop()

    assert status.state is (
        ConstitutionalRuntimeKernelState.STOPPED
    )
    assert status.running is False

    assert all(
        service.state.value == "stopped"
        for service in kernel.service_registry.all()
    )


def test_invalid_start_is_rejected() -> None:
    kernel = ConstitutionalRuntimeKernel()

    kernel.start()

    with pytest.raises(KernelLifecycleError):
        kernel.start()


def test_invalid_stop_is_rejected() -> None:
    kernel = ConstitutionalRuntimeKernel()

    with pytest.raises(KernelLifecycleError):
        kernel.stop()


def test_manual_composition() -> None:
    kernel = ConstitutionalRuntimeKernel(
        auto_compose=False
    )

    assert kernel.state is (
        ConstitutionalRuntimeKernelState.CREATED
    )

    kernel.compose()

    assert kernel.state is (
        ConstitutionalRuntimeKernelState.COMPOSED
    )


def test_double_composition_is_rejected() -> None:
    kernel = ConstitutionalRuntimeKernel()

    with pytest.raises(KernelLifecycleError):
        kernel.compose()


def test_overview_is_available() -> None:
    kernel = ConstitutionalRuntimeKernel()

    overview = kernel.overview()

    assert "runtime" in overview
    assert "services" in overview
    assert "graph" in overview
    assert "health" in overview
    assert "intelligence" in overview


def test_snapshot_contains_complete_fabric() -> None:
    kernel = ConstitutionalRuntimeKernel()

    snapshot = kernel.snapshot()
    payload = snapshot.to_dict()

    assert "kernel" in payload
    assert "runtime" in payload
    assert "services" in payload
    assert "graph" in payload
    assert "events" in payload
    assert "twin" in payload
    assert "intelligence" in payload
    assert "missions" in payload
    assert "scheduler" in payload


def test_status_tracks_event_subscriber() -> None:
    kernel = ConstitutionalRuntimeKernel()

    status = kernel.status()

    assert status.event_subscribers >= 1
    assert status.twin_revision >= 0


def test_close_releases_twin_subscription() -> None:
    kernel = ConstitutionalRuntimeKernel()

    before = (
        kernel.event_bus
        .statistics()
        .subscriber_count
    )

    kernel.close()

    after = (
        kernel.event_bus
        .statistics()
        .subscriber_count
    )

    assert before >= 1
    assert after == before - 1


def test_kernel_does_not_absorb_subsystem_methods() -> None:
    kernel = ConstitutionalRuntimeKernel()

    forbidden = {
        "register",
        "transition",
        "report_health",
        "connect",
        "publish",
        "analyze",
        "enqueue_ready",
        "dequeue",
        "mark_succeeded",
        "mark_failed",
    }

    assert forbidden.isdisjoint(
        set(dir(kernel))
    )
