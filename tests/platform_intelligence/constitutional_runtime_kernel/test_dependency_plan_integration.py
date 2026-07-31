from __future__ import annotations

from aletheus.platform_intelligence import (
    ConstitutionalRuntimeKernel,
    ConstitutionalRuntimeKernelState,
    ConstitutionalState,
)


def test_kernel_exposes_dependency_manager() -> None:
    kernel = ConstitutionalRuntimeKernel()

    assert kernel.dependency_manager is not None
    assert kernel.dependency_manager.validate().valid is True


def test_kernel_boot_plan_contains_every_service() -> None:
    kernel = ConstitutionalRuntimeKernel()

    plan = kernel.boot_plan()

    assert plan.direction == "boot"
    assert plan.service_count == (kernel.service_registry.statistics().registered)

    assert set(plan.ordered_services) == {
        service.address for service in kernel.service_registry.all()
    }


def test_kernel_shutdown_plan_reverses_boot_levels() -> None:
    kernel = ConstitutionalRuntimeKernel()

    boot = kernel.boot_plan()
    shutdown = kernel.shutdown_plan()

    assert shutdown.direction == "shutdown"

    assert [level.services for level in shutdown.levels] == [
        level.services for level in reversed(boot.levels)
    ]


def test_kernel_starts_using_dependency_plan() -> None:
    kernel = ConstitutionalRuntimeKernel()

    status = kernel.start()

    assert status.state is (ConstitutionalRuntimeKernelState.RUNNING)

    assert all(
        service.state is ConstitutionalState.RUNNING
        for service in kernel.service_registry.all()
    )


def test_kernel_stops_using_dependency_plan() -> None:
    kernel = ConstitutionalRuntimeKernel()

    kernel.start()
    status = kernel.stop()

    assert status.state is (ConstitutionalRuntimeKernelState.STOPPED)

    assert all(
        service.state is ConstitutionalState.STOPPED
        for service in kernel.service_registry.all()
    )


def test_kernel_can_restart_after_stop() -> None:
    kernel = ConstitutionalRuntimeKernel()

    kernel.start()
    kernel.stop()
    status = kernel.start()

    assert status.state is (ConstitutionalRuntimeKernelState.RUNNING)

    assert all(
        service.state is ConstitutionalState.RUNNING
        for service in kernel.service_registry.all()
    )


def test_restart_plan_contains_target_and_dependents() -> None:
    kernel = ConstitutionalRuntimeKernel()

    plan = kernel.restart_plan("service.platform-intelligence.service-registry")

    assert plan.direction == "restart"
    assert "service.platform-intelligence.service-registry" in plan.ordered_services

    assert "service.platform-intelligence.digital-twin" in plan.ordered_services

    assert "service.platform-intelligence.runtime-explorer" in plan.ordered_services


def test_kernel_does_not_absorb_dependency_reasoning() -> None:
    kernel = ConstitutionalRuntimeKernel()

    forbidden = {
        "dependencies_of",
        "dependents_of",
        "validate_dependencies",
        "topological_sort",
        "find_cycles",
    }

    assert forbidden.isdisjoint(set(dir(kernel)))
